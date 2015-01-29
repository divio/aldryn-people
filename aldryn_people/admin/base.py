# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import get_language


class AllTranslationsAdminMixin(object):
    """To use this, apply this mixin to your Admin class, then add
    'all_translations' to your list_display list."""

    def all_translations(self, obj):
        """This is an adapter for the functionality that was in HVAD but not
        in Parler.
        """
        available = list(obj.get_available_languages())
        langs = []
        for lang, _ in settings.LANGUAGES:
            if lang in available:
                langs.append(lang)
                available.remove(lang)
        langs += available
        for idx, lang in enumerate(langs):
            change_form_url = reverse(
                'admin:{app_label}_{model_name}_change'.format(
                    app_label=obj._meta.app_label.lower(),
                    model_name=obj.__class__.__name__.lower(),
                ), args=(obj.id, )
            )
            link = '<a href="{url}?language={lang}">{lang}</a>'.format(
                url=change_form_url,
                lang=lang,
            )
            if lang == get_language():
                link = "<strong>{0}</strong>".format(link)
            langs[idx] = link
        return ', '.join(langs)
    all_translations.short_description = 'available translations'
    all_translations.allow_tags = True
