# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TransactionTestCase

from ..cms_toolbar import get_admin_url


class TestToolbarUtils(TransactionTestCase):

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
        self.assertIn('/admin/auth/user/1/?alpha=beta', url)

        # With pattern args and two URL parameters
        kwargs = {'alpha': 'beta', 'gamma': 'delta', }
        url = get_admin_url(change_action, args, **kwargs)
        self.assertIn('/admin/auth/user/1/?alpha=beta&gamma=delta', url)

        # With pattern args and 3 URL parameters
        kwargs = {'a': 'b', 'g': 'd', 'e': 'z', }
        url = get_admin_url(change_action, args, **kwargs)
        self.assertIn('/admin/auth/user/1/?a=b&e=z&g=d', url)

        # With pattern args and numerical URL params
        kwargs = {'a': 1, 'g': 2, 'e': 3, }
        url = get_admin_url(change_action, args, **kwargs)
        self.assertIn('/admin/auth/user/1/?a=1&e=3&g=2', url)

        # With pattern args and odd-typed URL params
        kwargs = {'a': [], 'g': {}, 'e': None}
        url = get_admin_url(change_action, args, **kwargs)
        self.assertIn('/admin/auth/user/1/?a=[]&e=None&g={}', url)

        # No pattern args...
        add_action = 'auth_user_add'
        kwargs = {'groups': 1, }
        url = get_admin_url(add_action, **kwargs)
        self.assertIn('/admin/auth/user/add/?groups=1', url)

        # No pattern args and no kwargs
        add_action = 'auth_user_add'
        url = get_admin_url(add_action)
        self.assertIn('/admin/auth/user/add/', url)
