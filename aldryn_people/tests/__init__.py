# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import IntegrityError
from django.test import RequestFactory, TestCase
from django.utils.translation import override

from cms import api
from cms.models import Title
from cms.test_utils.testcases import BaseCMSTestCase
from cms.utils import get_cms_setting
from cms.utils.i18n import get_language_list

from djangocms_helper.utils import create_user

from ..models import Group, Person


class BasePeopleTest(BaseCMSTestCase, TestCase):
    su_username = 'user'
    su_password = 'pass'

    data = {
        'group1': {
            'en': {'name': 'group1', 'description': 'description1'},
            'de': {'name': 'Gruppe1', 'description': 'Beschreibung1'},
        },
        'group2': {
            # This should *not* have a EN translation
            'de': {'name': 'Gruppe2', 'description': 'Beschreibung2'},
        },
        'person1': {
            'en': {'function': 'function1', 'description': 'description-en'},
            'de': {'function': 'Funktion1', 'description': 'Beschreibung-de'},
        },
        'person2': {
            # This should *not* have a EN translation
            'de': {'function': 'Funktion2', 'description': 'Beschreibung2'},
        },
    }

    @staticmethod
    def reload(obj, language=None):
        """Simple convenience method for re-fetching an object from the ORM,
        optionally "as" a specified language."""
        try:
            new_obj = obj.__class__.objects.language(language).get(id=obj.id)
        except:
            new_obj = obj.__class__.objects.get(id=obj.id)
        return new_obj

    def assertEqualItems(self, a, b):
        try:
            # In Python3, this method has been renamed (poorly)
            return self.assertCountEqual(a, b)
        except:
            # In 2.6, assertItemsEqual() doesn't sort first
            return self.assertItemsEqual(sorted(a), sorted(b))

    def mktranslation(self, obj, lang, **kwargs):
        """Simple method of adding a translation to an existing object."""
        try:
            obj.set_current_language(lang)
        except:
            try:
                obj.translate(lang)
            except IntegrityError:
                pass
        for k, v in kwargs.items():
            setattr(obj, k, v)
        obj.save()

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.page = api.create_page(
            'page', self.template, self.language, published=True)
        self.placeholder = self.page.placeholders.all()[0]
        self.superuser = self.create_superuser()
        with override('en'):
            self.person1 = Person(**self.data['person1']['en'])
            self.group1 = Group(**self.data['group1']['en'])
        self.person1.name = 'person1'
        self.person1.slug = 'person1-slug'
        self.person1.save()
        self.group1.save()

        # Add a DE translation for person1, group1
        self.mktranslation(self.person1, 'de', **self.data['person1']['de'])
        self.mktranslation(self.group1, 'de', **self.data['group1']['de'])

        # Make person2, group2
        with override('de'):
            self.person2 = Person(**self.data['person2']['de'])
            self.group2 = Group(**self.data['group2']['de'])
        self.person2.name = 'person2'
        self.person2.slug = 'person2-slug'
        self.person2.save()
        self.group2.save()

    def tearDown(self):
        Person.objects.all().delete()
        Group.objects.all().delete()

    def create_superuser(self):
        return User.objects.create_superuser(
            self.su_username, 'email@example.com', self.su_password)


class CMSRequestBasedTest(TestCase):
    """Sets-up User(s) and CMS Pages for testing."""
    languages = get_language_list()

    @classmethod
    def setUpClass(cls):
        cls.request_factory = RequestFactory()
        cls.user = create_user('normal', 'normal@admin.com', 'normal')
        cls.site1 = Site.objects.get(pk=1)

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()

    def get_or_create_page(self, base_title=None, languages=None):
        """Creates a page with a given title, or, if it already exists, just
        retrieves and returns it."""
        from cms.api import create_page, create_title
        if not base_title:
            # No title? Create one.
            base_title = self.rand_str(prefix="page", length=8)
        if not languages:
            # If no langs supplied, use'em all
            languages = self.languages
        # If there is already a page with this title, just return it.
        try:
            page_title = Title.objects.get(title=base_title)
            return page_title.page.get_draft_object()
        except:
            pass

        # No? Okay, create one.
        page = create_page(base_title, 'fullwidth.html', language=languages[0])
        # If there are multiple languages, create the translations
        if len(languages) > 1:
            for lang in languages[1:]:
                title_lang = "{0}-{1}".format(base_title, lang)
                create_title(language=lang, title=title_lang, page=page)
                page.publish(lang)
        return page.get_draft_object()

    def get_page_request(
            self, page, user, path=None, edit=False, lang_code='en'):
        from cms.middleware.toolbar import ToolbarMiddleware
        path = path or page and page.get_absolute_url()
        if edit:
            path += '?edit'
        request = RequestFactory().get(path)
        request.session = {}
        request.user = user
        request.LANGUAGE_CODE = lang_code
        if edit:
            request.GET = {'edit': None}
        else:
            request.GET = {'edit_off': None}
        request.current_page = page
        mid = ToolbarMiddleware()
        mid.process_request(request)
        return request
