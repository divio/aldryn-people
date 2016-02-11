# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from distutils.version import LooseVersion

from django import get_version
from django.test import TransactionTestCase

from ..cms_toolbar import get_admin_url


DJANGO_1_9_OR_HIGHER = (
    LooseVersion(get_version()) >= LooseVersion('1.9')
)


class TestToolbarUtils(TransactionTestCase):

    def build_expected_admin_change_url(self, user_id, params=None):
        """
        Returns admin change url valid for different django versions.
        :param user_id: user_id/pk
        :param params: unique part of url.
        :return: sting url
        """
        params = '?{0}'.format(params) if params else ''
        if DJANGO_1_9_OR_HIGHER:
            base_url = '/admin/auth/user/{0}/change/{1}'
        else:
            base_url = '/admin/auth/user/{0}/{1}'
        return base_url.format(user_id, params)

    def test_get_admin_url(self):
        # With pattern args, but no URL parameters
        change_action = 'auth_user_change'
        args = [1, ]
        kwargs = {}
        url = get_admin_url(change_action, args, **kwargs)
        self.assertIn('/admin/auth/user/1/', url)

        # With pattern args and a single URL parameter
        kwargs = {'alpha': 'beta', }
        url = get_admin_url(change_action, args, **kwargs)
        expected_url = self.build_expected_admin_change_url(1, 'alpha=beta')
        self.assertIn(expected_url, url)

        # With pattern args and two URL parameters
        kwargs = {'alpha': 'beta', 'gamma': 'delta', }
        url = get_admin_url(change_action, args, **kwargs)
        expected_url = self.build_expected_admin_change_url(
            1, 'alpha=beta&gamma=delta')
        self.assertIn(expected_url, url)

        # With pattern args and 3 URL parameters
        kwargs = {'a': 'b', 'g': 'd', 'e': 'z', }
        url = get_admin_url(change_action, args, **kwargs)
        expected_url = self.build_expected_admin_change_url(1, 'a=b&e=z&g=d')
        self.assertIn(expected_url, url)

        # With pattern args and numerical URL params
        kwargs = {'a': 1, 'g': 2, 'e': 3, }
        url = get_admin_url(change_action, args, **kwargs)
        expected_url = self.build_expected_admin_change_url(1, 'a=1&e=3&g=2')
        self.assertIn(expected_url, url)

        # With pattern args and odd-typed URL params
        kwargs = {'a': [], 'g': {}, 'e': None}
        url = get_admin_url(change_action, args, **kwargs)
        expected_url = self.build_expected_admin_change_url(
            1, 'a=[]&e=None&g={}')
        self.assertIn(expected_url, url)

        # No pattern args...
        add_action = 'auth_user_add'
        kwargs = {'groups': 1, }
        url = get_admin_url(add_action, **kwargs)
        self.assertIn('/admin/auth/user/add/?groups=1', url)

        # No pattern args and no kwargs
        add_action = 'auth_user_add'
        url = get_admin_url(add_action)
        self.assertIn('/admin/auth/user/add/', url)
