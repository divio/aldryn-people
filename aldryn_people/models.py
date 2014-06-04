# -*- coding: utf-8 -*-
import base64
import urlparse
import vobject

from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField
from hvad.models import TranslatableModel, TranslatedFields
from sortedm2m.fields import SortedManyToManyField

from .utils import get_additional_styles


class Group(TranslatableModel):
    translations = TranslatedFields(
        company_name=models.CharField(_('company name'), max_length=255),
        company_description=HTMLField(_('company description'), blank=True),
    )
    address = models.TextField(verbose_name=_('address'), blank=True)
    postal_code = models.CharField(verbose_name=_('postal code'), max_length=20, blank=True)
    city = models.CharField(verbose_name=_('city'), max_length=255, blank=True)
    phone = models.CharField(verbose_name=_('phone'), null=True, blank=True, max_length=100)
    fax = models.CharField(verbose_name=_('fax'), null=True, blank=True, max_length=100)
    email = models.EmailField(verbose_name=_('email'), blank=True, default='')
    website = models.URLField(verbose_name=_('website'), null=True, blank=True)

    def __unicode__(self):
        return self.lazy_translation_getter('company_name', str(self.pk))

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')


class Person(TranslatableModel):
    translations = TranslatedFields(
        function=models.CharField(_('function'), max_length=255, blank=True, default=''),
        description=HTMLField(_('Description'), blank=True, default='')
    )
    name = models.CharField(verbose_name=_('name'), max_length=255)
    phone = models.CharField(verbose_name=_('phone'), null=True, blank=True, max_length=100)
    mobile = models.CharField(verbose_name=_('mobile'), null=True, blank=True, max_length=100)
    fax = models.CharField(verbose_name=_('fax'), null=True, blank=True, max_length=100)
    email = models.EmailField(verbose_name=_("email"), blank=True, default='')
    website = models.URLField(verbose_name=_('website'), null=True, blank=True)
    group = models.ForeignKey(Group, verbose_name=_('group'),
                              blank=True, null=True)
    visual = FilerImageField(null=True, blank=True, default=None, on_delete=models.SET_NULL)
    slug = models.CharField(verbose_name=_('unique slug'), max_length=255, blank=True, null=True, unique=True)
    vcard_enabled = models.BooleanField(verbose_name=_('enable vCard download'), default=True)
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), null=True, blank=True, unique=True)

    def __unicode__(self):
        return self.name

    @property
    def comment(self):
        return self.lazy_translation_getter('description', '')

    def get_absolute_url(self):
        if self.slug:
            kwargs = {'slug': self.slug}
        else:
            kwargs = {'pk': self.pk}
        return reverse('detail', kwargs=kwargs)

    def get_vcard(self, request=None):
        company_name = self.group.lazy_translation_getter('company_name')
        function = self.lazy_translation_getter('function')

        vcard = vobject.vCard()
        vcard.add('n').value = vobject.vcard.Name(given=self.name)
        vcard.add('fn').value = self.name

        if self.visual:
            try:
                with open(self.visual.path, 'rb') as f:
                    photo = vcard.add('photo')
                    photo.type_param = self.visual.extension.upper()
                    photo.value = base64.b64encode(f.read())
                    photo.encoded = True
                    photo.encoding_param = 'B'
            except IOError:
                if request:
                    photo = vcard.add('photo')
                    photo.type_param = self.visual.extension.upper()
                    photo.value = urlparse.urljoin(request.build_absolute_uri(), self.visual.url)

        if self.email:
            vcard.add('email').value = self.email
        if function:
            vcard.add('title').value = function
        if self.phone:
            tel = vcard.add('tel')
            tel.value = unicode(self.phone)
            tel.type_param = 'WORK'
        if self.mobile:
            tel = vcard.add('tel')
            tel.value = unicode(self.mobile)
            tel.type_param = 'CELL'
        if self.fax:
            fax = vcard.add('tel')
            fax.value = unicode(self.fax)
            fax.type_param = 'FAX'
        if self.website:
            website = vcard.add('url')
            website.value = unicode(self.website)

        if self.group:
            if company_name:
                vcard.add('org').value = [company_name]
            if self.group.address or self.group.city or self.group.postal_code:
                vcard.add('adr')
                vcard.adr.type_param = 'WORK'
                vcard.adr.value = vobject.vcard.Address()
                if self.group.address:
                    vcard.adr.value.street = self.group.address
                if self.group.city:
                    vcard.adr.value.city = self.group.city
                if self.group.postal_code:
                    vcard.adr.value.code = self.group.postal_code
            if self.group.phone:
                tel = vcard.add('tel')
                tel.value = unicode(self.group.phone)
                tel.type_param = 'WORK'
            if self.group.fax:
                fax = vcard.add('tel')
                fax.value = unicode(self.group.fax)
                fax.type_param = 'FAX'
            if self.group.website:
                website = vcard.add('url')
                website.value = unicode(self.group.website)

        return vcard.serialize()

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')


class PeoplePlugin(CMSPlugin):

    STYLE_CHOICES = [
        ('standard', _('Standard')),
        ('feature', _('Feature'))
    ] + get_additional_styles()

    style = models.CharField(
        _('Style'), choices=STYLE_CHOICES, default=STYLE_CHOICES[0][0], max_length=50)
    people = SortedManyToManyField(Person, blank=True, null=True)
    group_by_group = models.BooleanField(
        verbose_name=_('group by group'),
        default=True,
        help_text=_('when checked, people are grouped by their group')
    )
    show_links = models.BooleanField(verbose_name=_('Show links to Detail Page'), default=False)
    show_vcard = models.BooleanField(verbose_name=_('Show links to download vCard'), default=False)

    def __unicode__(self):
        return str(self.pk)

    def copy_relations(self, oldinstance):
        self.people = oldinstance.people.all()
