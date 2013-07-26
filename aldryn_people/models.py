# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from phonenumber_field.modelfields import PhoneNumberField
from hvad.models import TranslatableModel, TranslatedFields

import vobject


class Group(TranslatableModel):
    translations = TranslatedFields(
        company_name=models.CharField(_('company name'), max_length=255),
    )
    address = models.TextField(verbose_name=_('address'))
    postal_code = models.CharField(verbose_name=_('postal code'), max_length=20)
    city = models.CharField(verbose_name=_('city'), max_length=255)
    phone = PhoneNumberField(verbose_name=_('phone'), null=True, blank=True)

    def __unicode__(self):
        return self.lazy_translation_getter('company_name', str(self.pk))

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')


class Person(TranslatableModel):

    translations = TranslatedFields(
        function=models.CharField(_('function'), max_length=255),
        comment=models.TextField(_('comment'), blank=True, default='')
    )
    name = models.CharField(verbose_name=_('name'), max_length=255)
    phone = PhoneNumberField(verbose_name=_('phone'), null=True, blank=True)
    mobile = PhoneNumberField(verbose_name=_('mobile'), null=True, blank=True)
    email = models.EmailField(verbose_name=_("email"))
    group = models.ForeignKey(Group, verbose_name=_('group'),
                              blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_vcard(self):
        vcard = vobject.vCard()
        vcard.add('n').value = vobject.vcard.Name(given=self.name)
        vcard.add('fn').value = self.name
        vcard.add('email').value = self.email
        vcard.add('title').value = self.function
        if self.phone:
            tel = vcard.add('tel')
            tel.value = unicode(self.phone)
            tel.type_param = 'HOME'
        if self.mobile:
            tel = vcard.add('tel')
            tel.value = unicode(self.mobile)
            tel.type_param = 'MOBILE'

        if self.group:
            vcard.add('org').value = [self.group.company_name]
            vcard.add('adr')
            vcard.adr.type_param = 'WORK'
            vcard.adr.value = vobject.vcard.Address(
                street=self.group.address,
                city=self.group.city,
                code=self.group.postal_code)
            if self.group.phone:
                tel = vcard.add('tel')
                tel.value = unicode(self.group.phone)
                tel.type_param = 'WORK'

        return vcard.serialize()

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')


class PeoplePlugin(CMSPlugin):
    people = models.ManyToManyField(Person, blank=True, null=True)

    def __unicode__(self):
        return str(self.pk)

    def copy_relations(self, oldinstance):
        self.people = oldinstance.people.all()
