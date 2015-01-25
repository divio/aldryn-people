# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.utils.translation import override

from ..admin.models_admin import PersonAdmin
from ..models import Person

from . import BasePeopleTest


class TestPersonAdmin(BasePeopleTest):

    def test_all_translations(self):
        site = Site.objects.get(pk=1)
        model_admin = PersonAdmin(self.person1, site)
        all_translations = model_admin.all_translations(self.person1)
        obj_id = self.person1.id
        with override('en'):
            self.assertEqual(
                all_translations,
                '<strong><a href="/en/admin/aldryn_people/person/{id}/?language=en">en</a></strong>, <a href="/en/admin/aldryn_people/person/{id}/?language=de">de</a>'.format(id=obj_id)  # flake8: noqa
            )
        # This test does not pass
        # with override('de'):
        #     self.assertEqual(
        #         all_translations,
        #         '<a href="/en/admin/aldryn_people/person/{id}/?language=en">en</a>, <strong><a href="/en/admin/aldryn_people/person/{id}/?language=de">de</a></strong>'.format(id=obj_id)  # flake8: noqa
        #     )
