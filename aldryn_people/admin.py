# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from hvad.admin import TranslatableAdmin

from .models import Person, Group
from .forms import PersonForm


class PersonAdmin(TranslatableAdmin):

    list_display = [
        '__str__', 'email', 'vcard_enabled', 'all_translations']
    list_filter = ['group', 'vcard_enabled']
    search_fields = ('name', 'email', 'translations__function')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('user',)

    fieldsets = (
        (None, {
            'fields': (
                'name', 'function', 'slug', 'visual', 'vcard_enabled'
            ),
        }),
        (_('Contact'), {
            'fields': (
                'phone', 'mobile', 'fax', 'email', 'website', 'user'
            ),
        }),
        (None, {
            'fields': (
                'group', 'description',
            ),
        }),
    )

    form = PersonForm


class GroupAdmin(TranslatableAdmin):

    list_display = ['__str__', 'city', 'all_translations']
    search_filter = ['name']

    fieldsets = (
        (None, {
            'fields': (
                'name', 'description', 'phone', 'fax', 'email', 'website'
            ),
        }),
        (_('Address'), {
            'fields': (
                'address', 'postal_code', 'city'
            ),
        }),
    )

admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)
