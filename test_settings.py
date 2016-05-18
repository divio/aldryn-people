# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django

from distutils.version import LooseVersion
from cms import __version__ as cms_string_version

cms_version = LooseVersion(cms_string_version)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:9001/solr/default',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'EXCLUDED_INDEXES': ['thirdpartyapp.search_indexes.BarIndex'],
    },
    'en': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://my-solr-server/solr/my-site-en/',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    },
    'de': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://my-solr-server/solr/my-site-de/',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    },
}

HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Zurich',
    'HAYSTACK_CONNECTIONS': HAYSTACK_CONNECTIONS,
    'INSTALLED_APPS': [
        'aldryn_common',
        'aldryn_reversion',
        'aldryn_translation_tools',
        'djangocms_text_ckeditor',
        'easy_thumbnails',
        'filer',
        'parler',
        'reversion',
        'sortedm2m',
    ],
    'THUMBNAIL_PROCESSORS': (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters',
    ),
    'CMS_PERMISSION': True,
    # 'ALDRYN_BOILERPLATE_NAME': 'bootstrap3',
    'LANGUAGES': (
        ('en', 'English'),
        ('de', 'German'),
        ('fr', 'French'),
    ),
    'CMS_LANGUAGES': {
        1: [
            {
                'code': 'de',
                'name': 'Deutsche',
                'fallbacks': ['en', ]  # FOR TESTING DO NOT ADD 'fr' HERE
            },
            {
                'code': 'fr',
                'name': 'Française',
                'fallbacks': ['en', ]  # FOR TESTING DO NOT ADD 'de' HERE
            },
            {
                'code': 'en',
                'name': 'English',
                'fallbacks': ['de', 'fr', ]
            },
            {
                'code': 'it',
                'name': 'Italiano',
                'fallbacks': ['fr', ]  # FOR TESTING, LEAVE AS ONLY 'fr'
            },
        ],
    },
    # app-specific
    'PARLER_LANGUAGES': {
        1: [
            {
                'code': u'en',
                'fallbacks': ['de', 'fr'],
                'hide_untranslated': False
            },
            {
                'code': u'fr',
                'fallbacks': [u'en'],
                'hide_untranslated': False
            },
            {
                'code': u'de',
                'fallbacks': [u'en'],
                'hide_untranslated': False
            }
        ],
        'default': {
            'code': u'en',
            'fallbacks': [u'en'],
            'hide_untranslated': False}
    },
    'PARLER_ENABLE_CACHING': False,
}

# This set of MW classes should work for Django 1.6 and 1.7.
MIDDLEWARE_CLASSES_16_17 = [
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware'
]

MIDDLEWARE_CLASSES_18 = [
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
]

# Use PEP 386-compliant version number
django_version = django.get_version()

if django_version.startswith('1.6.') or django_version.startswith('1.7.'):
    HELPER_SETTINGS['MIDDLEWARE_CLASSES'] = MIDDLEWARE_CLASSES_16_17
elif django_version.startswith('1.8.'):
    HELPER_SETTINGS['MIDDLEWARE_CLASSES'] = MIDDLEWARE_CLASSES_18

# If using CMS 3.2+, use the CMS middleware for ApphookReloading, otherwise,
# use aldryn_apphook_reload's.
if cms_version < LooseVersion('3.2.0'):
    HELPER_SETTINGS['MIDDLEWARE_CLASSES'].remove(
        'cms.middleware.utils.ApphookReloadMiddleware')
    HELPER_SETTINGS['MIDDLEWARE_CLASSES'].insert(
        0, 'aldryn_apphook_reload.middleware.ApphookReloadMiddleware')
    HELPER_SETTINGS['INSTALLED_APPS'].insert(
        0, 'aldryn_apphook_reload')


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_people')  # , extra_args=['--boilerplate']

if __name__ == "__main__":
    run()
