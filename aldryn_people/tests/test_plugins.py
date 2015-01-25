# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import force_text

from cms import api
from cms.models import CMSPlugin
from cms.test_utils.testcases import URL_CMS_PLUGIN_ADD

from ..models import Person
from ..cms_plugins import PeoplePlugin

from . import BasePeopleTest


class TestPersonPlugins(BasePeopleTest):

    def test_add_people_list_plugin_api(self):
        """
        We add a person to the People Plugin and look her up
        """
        name = 'Donald'
        Person.objects.create(name=name)
        plugin = api.add_plugin(self.placeholder, PeoplePlugin, self.language)
        plugin.people = Person.objects.all()
        self.assertEqual(force_text(plugin), force_text(plugin.pk))
        self.page.publish(self.language)

        url = self.page.get_absolute_url()
        response = self.client.get(url)
        self.assertContains(response, name)

    def test_add_people_list_plugin_client(self):
        """
        We log into the PeoplePlugin
        """
        self.client.login(username=self.su_username, password=self.su_password)

        plugin_data = {
            'plugin_type': 'PeoplePlugin',
            'plugin_language': self.language,
            'placeholder_id': self.placeholder.pk,
        }

        response = self.client.post(URL_CMS_PLUGIN_ADD, plugin_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CMSPlugin.objects.exists())
