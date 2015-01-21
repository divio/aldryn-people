# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from ..models import Person

from . import BasePeopleTest


class TestPersonAppHook(BasePeopleTest):

    def test_add_people_app(self):
        """
        We add a person to the app
        """
        self.page.application_urls = 'PeopleApp'
        self.page.publish(self.language)

        person = Person.objects.create(
            name='Michael', phone='0785214521', email='michael@mit.ch',
            slug='michael'
        )
        # By slug
        url = reverse('person-detail', kwargs={'slug': person.slug})
        response = self.client.get(url)
        self.assertContains(response, 'Michael')

        # By pk
        url = reverse('person-detail', kwargs={'pk': person.pk})
        response = self.client.get(url)
        self.assertContains(response, 'Michael')
