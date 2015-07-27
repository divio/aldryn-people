# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from parler.admin import TranslatableAdmin
from aldryn_translation_tools.admin import AllTranslationsMixin

from .models import Person, Group


class PersonAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_display = [
        '__str__', 'email', 'vcard_enabled', 'num_groups', ]
    list_filter = ['groups', 'vcard_enabled']
    search_fields = ('translations__name', 'email', 'translations__function')
    raw_id_fields = ('user',)

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'slug', ),
                'function', 'description',
            ),
        }),
        (_('Contact (untranslated)'), {
            'fields': (
                'visual', 'phone', 'mobile', 'fax', 'email', 'website',
                'user', 'vcard_enabled'
            ),
        }),
        (None, {
            'fields': (
                'groups',
            ),
        }),
    )

    def get_queryset(self, request):
        qs = super(PersonAdmin, self).queryset(request)
        qs = qs.annotate(group_count=Count('groups'))
        return qs

    def num_groups(self, obj):
        return obj.group_count
    num_groups.short_description = '# Groups'
    num_groups.admin_order_field = 'group_count'


class GroupAdmin(AllTranslationsMixin, TranslatableAdmin):

    list_display = ['__str__', 'city', 'num_people', ]
    search_filter = ['translations__name']
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'slug', ),
                'description',
            ),
        }),
        (_('Contact (untranslated)'), {
            'fields': (
                'phone', 'fax', 'email', 'website',
                'address', 'postal_code', 'city'
            )
        }),
    )

    def get_queryset(self, request):
        qs = super(GroupAdmin, self).queryset(request)
        qs = qs.annotate(people_count=Count('people'))
        return qs

    def num_people(self, obj):
        return obj.people_count
    num_people.short_description = '# People'
    num_people.admin_order_field = 'people_count'


admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)
