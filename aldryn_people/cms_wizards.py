# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from cms.wizards.wizard_pool import wizard_pool
from cms.wizards.wizard_base import Wizard

from parler.forms import TranslatableModelForm

from .models import Group, Person


class PeoplePersonWizard(Wizard):

    def user_has_add_permission(self, user, **kwargs):
        """
        Return True if the current user has permission to add a person.
        :param user: The current user
        :param kwargs: Ignored here
        :return: True if user has add permission, else False
        """
        if user.is_superuser or user.has_perm("aldryn_people.add_person"):
            return True
        return False


class PeopleGroupWizard(Wizard):

    def user_has_add_permission(self, user, **kwargs):
        """
        Return True if the current user has permission to add a group.
        :param user: The current user
        :param kwargs: Ignored here
        :return: True if user has add permission, else False
        """
        if user.is_superuser or user.has_perm("aldryn_people.add_group"):
            return True
        return False


class CreatePeoplePersonForm(TranslatableModelForm):
    class Meta:
        model = Person
        fields = ['name', 'function', 'description', 'phone', 'mobile',
                  'email', 'website', 'groups', 'visual']


class CreatePeopleGroupForm(TranslatableModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'address', 'postal_code', 'city',
                  'phone', 'email', 'website']


people_person_wizard = PeoplePersonWizard(
    title=_('New person'),
    weight=300,
    form=CreatePeoplePersonForm,
    description=_("Create a new person.")
)

wizard_pool.register(people_person_wizard)


people_group_wizard = PeopleGroupWizard(
    title=_('New group'),
    weight=300,
    form=CreatePeopleGroupForm,
    description=_("Create a new group.")
)

wizard_pool.register(people_group_wizard)
