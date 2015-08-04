# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_client import forms


class Form(forms.BaseForm):
    people_plugin_styles = forms.CharField(
        'List of additional people plugin styles (comma separated)',
        required=False
    )

    user_threshold = forms.NumberField(
        'Once there are this many users, change drop-down to ID input field',
        required=False, min_value=0
    )

    def to_settings(self, data, settings):
        settings['PEOPLE_PLUGIN_STYLES'] = data.get('people_plugin_styles', '')
        try:
            settings['ALDRYN_PEOPLE_USER_THRESHOLD'] = int(data.get(
                'user_threshold'))
        except (ValueError, TypeError):
            pass
        return settings
