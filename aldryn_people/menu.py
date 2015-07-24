# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import get_language_from_request, ugettext as _

from cms.menu_bases import CMSAttachMenu
from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from .models import Group, Person


class PersonMenu(CMSAttachMenu):
    """
    Provides an attachable menu of all people.
    """
    name = _('Aldryn People: Person Menu')

    def get_nodes(self, request):
        nodes = []
        language = get_language_from_request(request, check_path=True)
        persons = Person.objects.language(language)

        for person in persons:
            node = NavigationNode(
                person.safe_translation_getter(
                    'name', default=_('person: {0}').format(person.pk),
                    language_code=language),
                person.get_absolute_url(language=language),
                person.pk,
            )
            nodes.append(node)
        return nodes

menu_pool.register_menu(PersonMenu)


class GroupMenu(CMSAttachMenu):
    """
    Provides an attachable menu of all groups.
    """
    name = _('Aldryn People: Group Menu')

    def get_nodes(self, request):
        nodes = []
        language = get_language_from_request(request, check_path=True)
        groups = Group.objects.language(language)

        for group in groups:
            node = NavigationNode(
                group.safe_translation_getter(
                    'name', default=_('group: {0}').format(group.pk),
                    language_code=language),
                group.get_absolute_url(language=language),
                group.pk,
            )
            nodes.append(node)
        return nodes

menu_pool.register_menu(GroupMenu)
