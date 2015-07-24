# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import base64
import six
import urlparse
import vobject
import warnings

import reversion

from reversion.revisions import RegistrationError
from distutils.version import StrictVersion
from django import get_version
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.importlib import import_module

try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode
from django.utils.text import slugify as default_slugify
from django.utils.translation import ugettext_lazy as _, ugettext, override

from aldryn_common.slugs import unique_slugify
from aldryn_common.admin_fields.sortedm2m import SortedM2MModelField
from cms.models.pluginmodel import CMSPlugin
from cms.utils.i18n import get_current_language, get_languages
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField
from parler.models import TranslatableModel, TranslatedFields
from sortedm2m.fields import SortedManyToManyField
from aldryn_reversion.core import version_controlled_content

from .utils import get_additional_styles

LANGUAGE_CODES = [lang['code'] for lang in get_languages()]


strict_version = StrictVersion(get_version())

if strict_version < StrictVersion('1.7.0'):
    # Prior to 1.7 it is pretty straight forward
    user_model = get_user_model()
    revision_manager = reversion.default_revision_manager
    if user_model not in revision_manager.get_registered_models():
        reversion.register(user_model)
else:
    # otherwise it is a pain, but thanks to solution of getting model from
    # https://github.com/django-oscar/django-oscar/commit/c479a1
    # we can do almost the same thing from the different side.
    from django.apps import apps
    from django.apps.config import MODELS_MODULE_NAME
    from django.core.exceptions import AppRegistryNotReady

    def get_model(app_label, model_name):
        """
        Fetches a Django model using the app registry.
        This doesn't require that an app with the given app label exists,
        which makes it safe to call when the registry is being populated.
        All other methods to access models might raise an exception about the
        registry not being ready yet.
        Raises LookupError if model isn't found.
        """
        try:
            return apps.get_model(app_label, model_name)
        except AppRegistryNotReady:
            if apps.apps_ready and not apps.models_ready:
                # If this function is called while `apps.populate()` is
                # loading models, ensure that the module that defines the
                # target model has been imported and try looking the model up
                # in the app registry. This effectively emulates
                # `from path.to.app.models import Model` where we use
                # `Model = get_model('app', 'Model')` instead.
                app_config = apps.get_app_config(app_label)
                # `app_config.import_models()` cannot be used here because it
                # would interfere with `apps.populate()`.
                import_module('%s.%s' % (app_config.name, MODELS_MODULE_NAME))
                # In order to account for case-insensitivity of model_name,
                # look up the model through a private API of the app registry.
                return apps.get_registered_model(app_label, model_name)
            else:
                # This must be a different case (e.g. the model really doesn't
                # exist). We just re-raise the exception.
                raise

    # now get the real user model
    user_model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
    model_app_name, model_model = user_model.split('.')
    user_model_object = get_model(model_app_name, model_model)
    # and try to register, if we have a registration error - that means that
    # it has been registered already
    try:
        reversion.register(user_model_object)
    except RegistrationError:
        pass


@version_controlled_content
@python_2_unicode_compatible
class Group(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_('name'), max_length=255),
        description=HTMLField(_('description'), blank=True),
        slug=models.SlugField(_('slug'), max_length=255, default=''),
    )
    address = models.TextField(
        verbose_name=_('address'), blank=True)
    postal_code = models.CharField(
        verbose_name=_('postal code'), max_length=20, blank=True)
    city = models.CharField(
        verbose_name=_('city'), max_length=255, blank=True)
    phone = models.CharField(
        verbose_name=_('phone'), null=True, blank=True, max_length=100)
    fax = models.CharField(
        verbose_name=_('fax'), null=True, blank=True, max_length=100)
    email = models.EmailField(
        verbose_name=_('email'), blank=True, default='')
    website = models.URLField(
        verbose_name=_('website'), null=True, blank=True)

    @property
    def company_name(self):
        warnings.warn(
            '"Group.company_name" has been refactored to "Group.name"',
            DeprecationWarning
        )
        return self.safe_translation_getter('name')

    @property
    def company_description(self):
        warnings.warn(
            '"Group.company_description" has been refactored to '
            '"Group.description"',
            DeprecationWarning
        )
        return self.safe_translation_getter('description')

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')

    def __str__(self):
        return self.safe_translation_getter(
            'name', default=_('Group: {0}').format(self.pk))

    def get_absolute_url(self, language=None):
        if not language:
            language = get_current_language()
        slug = self.safe_translation_getter(
            'slug', None, language_code=language, any_language=False)
        if slug:
            kwargs = {'slug': slug}
        else:
            kwargs = {'pk': self.pk}
        with override(language):
            return reverse('aldryn_people:group-detail', kwargs=kwargs)

    def slugify(self, source_text, i=None):
        slug = default_slugify(source_text)
        if i is not None:
            slug += "_%d" % i
        return slug

    def save(self, **kwargs):
        language = self.get_current_language()
        if not self.slug:
            self.slug = force_unicode(default_slugify(self.name))
        # If there is still no slug, we must give it something to start with
        if not self.slug:
            self.slug = ugettext('unnamed-group')
        if not Group.objects.language(language).filter(
                translations__slug=self.slug).exclude(pk=self.pk).exists():
            return super(Group, self).save(**kwargs)
        for lang in LANGUAGE_CODES:
            #
            # We'd much rather just do something like:
            # Group.objects.translated(lang, slug__startswith=self.slug)
            # But sadly, this isn't supported by Parler/Django, see:
            # http://django-parler.readthedocs.org/en/latest/api/\
            #     parler.managers.html#the-translatablequeryset-class
            #
            slugs = []
            all_slugs = (
                Group.objects.language(lang)
                             .exclude(pk=self.pk)
                             .values_list('translations__slug', flat=True)
            )
            for slug in all_slugs:
                if slug and slug.startswith((self.name, self.slug)):
                    slugs.append(slug)
            i = 1
            while True:
                slug = self.slugify(self.name or self.slug, i)
                if slug not in slugs:
                    self.slug = slug
                    return super(Group, self).save(**kwargs)
                i += 1


@version_controlled_content(follow=['groups', 'user'])
@python_2_unicode_compatible
class Person(TranslatableModel):
    translations = TranslatedFields(
        function=models.CharField(
            _('function'), max_length=255, blank=True, default=''),
        description=HTMLField(
            _('Description'), blank=True, default='')
    )
    name = models.CharField(
        verbose_name=_('name'), max_length=255)
    phone = models.CharField(
        verbose_name=_('phone'), null=True, blank=True, max_length=100)
    mobile = models.CharField(
        verbose_name=_('mobile'), null=True, blank=True, max_length=100)
    fax = models.CharField(
        verbose_name=_('fax'), null=True, blank=True, max_length=100)
    email = models.EmailField(
        verbose_name=_("email"), blank=True, default='')
    website = models.URLField(
        verbose_name=_('website'), null=True, blank=True)
    groups = SortedManyToManyField(
        'aldryn_people.Group', default=None, blank=True, related_name='people',
        help_text=_('Choose and order the groups for this person, the first '
                    'will be the "primary group".'))
    visual = FilerImageField(
        null=True, blank=True, default=None, on_delete=models.SET_NULL)
    slug = models.CharField(
        verbose_name=_('unique slug'), max_length=255, blank=True, null=True,
        unique=True)
    vcard_enabled = models.BooleanField(
        verbose_name=_('enable vCard download'), default=True)
    user = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        null=True, blank=True, unique=True, related_name='persons')

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')

    def __str__(self):
        pkstr = str(self.pk)

        if six.PY2:
            pkstr = six.u(pkstr)
        name = self.name.strip()
        return name if len(name) > 0 else pkstr

    @property
    def primary_group(self):
        """Simply returns the first in `groups`, if any, else None."""
        return self.groups.first()

    @property
    def comment(self):
        return self.safe_translation_getter('description', '')

    def get_absolute_url(self, language=None):
        if not language:
            language = get_current_language()
        if self.slug:
            kwargs = {'slug': self.slug}
        else:
            kwargs = {'pk': self.pk}
        with override(language):
            return reverse('aldryn_people:person-detail', kwargs=kwargs)

    def get_vcard(self, request=None):
        if self.primary_group:
            group_name = self.primary_group.safe_translation_getter('name')
        else:
            group_name = ''
        function = self.safe_translation_getter('function')

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
                    photo.value = urlparse.urljoin(
                        request.build_absolute_uri(), self.visual.url)

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

        if self.primary_group:
            if group_name:
                vcard.add('org').value = [group_name]
            if (self.primary_group.address or self.primary_group.city or
                    self.primary_group.postal_code):
                vcard.add('adr')
                vcard.adr.type_param = 'WORK'
                vcard.adr.value = vobject.vcard.Address()
                if self.primary_group.address:
                    vcard.adr.value.street = self.primary_group.address
                if self.primary_group.city:
                    vcard.adr.value.city = self.primary_group.city
                if self.primary_group.postal_code:
                    vcard.adr.value.code = self.primary_group.postal_code
            if self.primary_group.phone:
                tel = vcard.add('tel')
                tel.value = unicode(self.primary_group.phone)
                tel.type_param = 'WORK'
            if self.primary_group.fax:
                fax = vcard.add('tel')
                fax.value = unicode(self.primary_group.fax)
                fax.type_param = 'FAX'
            if self.primary_group.website:
                website = vcard.add('url')
                website.value = unicode(self.primary_group.website)

        return vcard.serialize()

    def save(self, **kwargs):
        if not self.slug:
            unique_slugify(instance=self, value=self.name)
        return super(Person, self).save(**kwargs)


@python_2_unicode_compatible
class BasePeoplePlugin(CMSPlugin):

    STYLE_CHOICES = [
        ('standard', _('Standard')),
        ('feature', _('Feature'))
    ] + get_additional_styles()

    style = models.CharField(
        _('Style'), choices=STYLE_CHOICES,
        default=STYLE_CHOICES[0][0], max_length=50)
    people = SortedM2MModelField(
        Person, blank=True, null=True)
    group_by_group = models.BooleanField(
        verbose_name=_('group by group'),
        default=True,
        help_text=_('when checked, people are grouped by their group')
    )
    show_links = models.BooleanField(
        verbose_name=_('Show links to Detail Page'), default=False)
    show_vcard = models.BooleanField(
        verbose_name=_('Show links to download vCard'), default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return unicode(self.pk)

    def copy_relations(self, oldinstance):
        self.people = oldinstance.people.all()

    def get_selected_people(self):
        return self.people.select_related('group', 'visual')


class PeoplePlugin(BasePeoplePlugin):

    class Meta:
        abstract = False
