# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext as _, get_language_from_request

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse
from parler.models import TranslatableModel

from .models import Group, Person


def get_obj_from_request(model, request,
                         pk_url_kwarg='pk',
                         slug_url_kwarg='slug',
                         slug_field='slug'):
    """
    Given a model and the request, try to extract and return an object
    from an available 'pk' or 'slug', or return None.

    Note that no checking is done that the view's kwargs really are for objects
    matching the provided model (how would it?) so use only where appropriate.
    """
    language = get_language_from_request(request, check_path=True)
    kwargs = request.resolver_match.kwargs
    mgr = model.objects
    if pk_url_kwarg in kwargs:
        return mgr.filter(pk=kwargs[pk_url_kwarg]).first()
    elif slug_url_kwarg in kwargs:
        # If the model is translatable, and the given slug is a translated
        # field, then find it the Parler way.
        filter_kwargs = {slug_field: kwargs[slug_url_kwarg]}
        translated_fields = model._parler_meta.get_translated_fields()
        if (issubclass(model, TranslatableModel) and
                slug_url_kwarg in translated_fields):
            return mgr.translated(language, **filter_kwargs).first()
        else:
            # OK, do it the normal way.
            return mgr.filter(**filter_kwargs).first()
    else:
        return None


@toolbar_pool.register
class PeopleToolbar(CMSToolbar):
    # watch_models must be a list, not a tuple
    # see https://github.com/divio/django-cms/issues/4135
    watch_models = [Person, Group, ]
    supported_apps = ('aldryn_people', )

    def populate(self):
        user = getattr(self.request, 'user', None)
        if user:
            view_name = self.request.resolver_match.view_name
            group = person = None
            if view_name == 'aldryn_people:group-detail':
                group = get_obj_from_request(Group, self.request)
            elif view_name in [
                    'aldryn_people:person-detail',
                    'aldryn_people:download_vcard']:
                person = get_obj_from_request(Person, self.request)
                if person and person.groups:
                    group = person.primary_group
            elif view_name in ['aldryn_people:group-list', ]:
                pass
            else:
                # We don't appear to be on any aldryn_people views so this
                # menu shouldn't even be here.
                return

            menu = self.toolbar.get_or_create_menu('people-app', "People")
            change_group_perm = user.has_perm('aldryn_people.change_group')
            add_group_perm = user.has_perm('aldryn_people.add_group')
            group_perms = [change_group_perm, add_group_perm]

            change_person_perm = user.has_perm('aldryn_people.change_person')
            add_person_perm = user.has_perm('aldryn_people.add_person')
            person_perms = [change_person_perm, add_person_perm]

            if change_group_perm:
                menu.add_sideframe_item(
                    _('Group list'),
                    url=admin_reverse('aldryn_people_group_changelist')
                )

            if add_group_perm:
                menu.add_modal_item(
                    _('Add new group'),
                    url=admin_reverse('aldryn_people_group_add')
                )

            if change_group_perm and group:
                menu.add_modal_item(
                    _('Edit group'),
                    admin_reverse('aldryn_people_group_change',
                                  args=(group.pk, )),
                    active=True,
                )

            if any(group_perms) and any(person_perms):
                menu.add_break()

            if change_person_perm:
                menu.add_sideframe_item(
                    _('Person list'),
                    url=admin_reverse('aldryn_people_person_changelist')
                )

            if add_person_perm:
                base_url = admin_reverse('aldryn_people_person_add')
                if group:
                    url = "{0}?groups={1}".format(base_url, group.pk)
                else:
                    url = base_url
                menu.add_modal_item(_('Add new person'), url=url)

            if change_person_perm and person:
                menu.add_modal_item(
                    _('Edit person'),
                    admin_reverse('aldryn_people_person_change',
                                  args=(person.pk,)),
                    active=True,
                )
