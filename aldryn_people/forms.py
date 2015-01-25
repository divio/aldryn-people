# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from parler.forms import TranslatableModelForm

from .models import Person


class PersonForm(TranslatableModelForm):
    class Meta:
        model = Person

    def clean_slug(self):
        return self.cleaned_data['slug'] or None
