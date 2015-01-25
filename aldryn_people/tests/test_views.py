# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import Http404
from django.test.client import RequestFactory

from ..views import DownloadVcardView

from . import BasePeopleTest, CMSRequestBasedTest


class TestDownloadVcardView(BasePeopleTest, CMSRequestBasedTest):
    def test_as_view(self):
        """Tests that DownloadVcardView produces the correct headers."""
        person1 = self.reload(self.person1, "en")
        person1.slug = 'person1-slug'
        kwargs = {"slug": person1.slug}
        person1_url = reverse('aldryn_people:person-detail', kwargs=kwargs)
        factory = RequestFactory()
        request = factory.get(person1_url)
        response = DownloadVcardView.as_view()(request, **kwargs)
        filename = '{0}.vcf'.format(person1.name)
        self.assertEqual(
            response["Content-Disposition"],
            'attachment; filename="{0}"'.format(filename)
        )
        # Now, disable vcards for this person, and re-test
        person1.vcard_enabled = False
        person1.save()
        with self.assertRaises(Http404):
            request = factory.get(person1_url)
            response = DownloadVcardView.as_view()(request, **kwargs)
