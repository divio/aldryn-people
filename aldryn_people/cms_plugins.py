# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from aldryn_people import models


class PeoplePlugin(CMSPluginBase):

    module = 'People'
    render_template = 'aldryn_people/plugins/people.html'
    name = _('Renders a list of people')
    model = models.PeoplePlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['people'] = instance.people.select_related('group')
        try:
            reverse('download_vcard', args=(1,))
            context['show_vcard'] = True
        except NoReverseMatch:
            pass
        return context

plugin_pool.register_plugin(PeoplePlugin)