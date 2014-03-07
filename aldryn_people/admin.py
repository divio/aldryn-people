# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from hvad.admin import TranslatableAdmin

from .models import Person, Group
from .forms import PersonForm


class PersonAdmin(TranslatableAdmin):

    list_display = ['__unicode__', 'email', 'all_translations']
    list_filter = ['group']
    search_fields = ('name', 'email', 'translations__function')

    fieldsets = (
        (None, {'fields': ('name', 'function', 'slug', 'visual')}),
        (_('Contact'), {'fields': ('phone', 'mobile', 'email')}),
        (None, {'fields': ('group', 'comment',)}),
    )

    form = PersonForm


class GroupAdmin(TranslatableAdmin):

    list_display = ['__unicode__', 'city', 'all_translations']
    search_filter = ['company_name']

    fieldsets = (
        (None, {'fields': ('company_name', 'company_description', 'phone')}),
        (_('Address'), {'fields': ('address', 'postal_code', 'city')}),
    )

admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)
