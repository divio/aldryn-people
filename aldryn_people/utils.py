# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings


def get_additional_styles():
    """
    Get additional styles choices from settings
    """
    styles = getattr(settings, 'PEOPLE_PLUGIN_STYLES', '')
    choices = [(s.strip().lower(), s.title()) for s in styles.split(',') if s]
    return choices
