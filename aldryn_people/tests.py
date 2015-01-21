# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from cms import api
from cms.utils import get_cms_setting
from cms.models import CMSPlugin
from cms.test_utils.testcases import BaseCMSTestCase, URL_CMS_PLUGIN_ADD

from .models import Person, Group
from .cms_plugins import PeoplePlugin


class PeopleAddTest(TestCase, BaseCMSTestCase):
    su_username = 'user'
    su_password = 'pass'

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.page = api.create_page('page', self.template, self.language, published=True)
        self.placeholder = self.page.placeholders.all()[0]
        self.superuser = self.create_superuser()

    def create_superuser(self):
        return User.objects.create_superuser(self.su_username, 'email@example.com', self.su_password)

    def test_create_person(self):
        """
        We can create a person with a name
        """
        name = 'Tom Test'
        person = Person.objects.create(name=name)
        self.assertEqual(person.name, name)
        self.assertEqual(Person.objects.all()[0], person)

    def test_delete_person(self):
        """
        We can delete a person
        """
        name = 'Person Delete'
        Person.objects.create(name=name)
        Person.objects.get(name=name).delete()
        self.assertFalse(Person.objects.filter(name=name))

    def test_create_group(self):
        """
        We can create a group with a name
        """
        group = Group.objects.create(name='group_b')
        self.assertTrue(group.name, 'group_b')

    def test_delete_group(self):
        """
        We can delete a group
        """
        name = 'Gruop Delete'
        Group.objects.create(name=name)
        Group.objects.using_translations().get(name=name).delete()
        self.assertFalse(Group.objects.using_translations().filter(name=name))

    def test_add_people_app(self):
        """
        We add a person to the app
        """
        self.page.application_urls = 'PeopleApp'
        self.page.publish(self.language)

        person = Person.objects.create(name='michael', phone='0785214521', email='michael@mit.ch')

        url = reverse('person-detail', kwargs={'pk': person.pk})
        response = self.client.get(url)
        self.assertContains(response, 'michael')

    def test_create_another_group(self):
        """
        we create a group
        """
        name = 'Gruppe Neu'
        group = Group.objects.create(name=name)
        self.assertEqual(group.name, name)
        self.assertEqual(Group.objects.all()[0], group)

    def test_add_person_to_group(self):
        """
        We create a person and add her to the created group
        """
        personname = 'Daniel'
        person = Person.objects.create(name=personname)
        name = 'Group One'
        group = Group.objects.create(name=name)
        person.group = group
        person.save()
        self.assertIn(person, group.person_set.all())

    def test_add_people_list_plugin_api(self):
        """
        We add a person to the People Plugin and look her up
        """
        name = 'Donald'
        Person.objects.create(name=name)
        plugin = api.add_plugin(self.placeholder, PeoplePlugin, self.language)
        plugin.people = Person.objects.all()
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
