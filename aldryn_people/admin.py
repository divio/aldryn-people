# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from aldryn_people.models import Person, Group

from hvad.admin import TranslatableAdmin


class PersonAdmin(TranslatableAdmin):

    list_display = ['__unicode__', 'email', 'all_translations']
    list_filter = ['group']
    search_fields = ('name', 'email', 'function')

    fieldsets = (
        (None, {'fields': ('name', 'function')}),
        (_('Contact'), {'fields': ('phone', 'mobile', 'email')}),
        (None, {'fields': ('group', 'comment',)}),
    )


class GroupAdmin(TranslatableAdmin):

    list_display = ['__unicode__', 'city', 'all_translations']
    search_filter = ['company_name']

    fieldsets = (
        (None, {'fields': ('company_name', 'phone')}),
        (_('Address'), {'fields': ('address', 'postal_code', 'city')}),
    )

admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)
