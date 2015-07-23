# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_client import forms


class Form(forms.BaseForm):
    people_plugin_styles = forms.CharField(
        'List of additional people plugin styles (comma separated)',
        required=False
    )

    def to_settings(self, data, settings):
        settings['PEOPLE_PLUGIN_STYLES'] = data.get('people_plugin_styles', '')
        return settings
