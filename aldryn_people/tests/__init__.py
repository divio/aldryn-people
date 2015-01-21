# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from cms import api
from cms.utils import get_cms_setting
from cms.test_utils.testcases import BaseCMSTestCase


class BasePeopleTest(TestCase, BaseCMSTestCase):
    su_username = 'user'
    su_password = 'pass'

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.page = api.create_page(
            'page', self.template, self.language, published=True)
        self.placeholder = self.page.placeholders.all()[0]
        self.superuser = self.create_superuser()

    def create_superuser(self):
        return User.objects.create_superuser(
            self.su_username, 'email@example.com', self.su_password)
