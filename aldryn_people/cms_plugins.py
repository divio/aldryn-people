# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import defaultdict

from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from aldryn_people import models


class PeoplePlugin(CMSPluginBase):

    TEMPLATE_NAME = 'aldryn_people/plugins/%s/people_list.html'
    module = 'People'
    render_template = TEMPLATE_NAME % models.PeoplePlugin.STYLE_CHOICES[0][0]
    name = _('People list')
    model = models.PeoplePlugin

    def group_people(self, people, language):
        groups = defaultdict(list)

        for people in people:
            groups[people.group].append(people)

        # Python/Django bug ?
        groups.default_factory = None
        return groups

    def render(self, context, instance, placeholder):
        people = instance.get_selected_people()
        self.render_template = self.TEMPLATE_NAME % instance.style

        context['instance'] = instance
        context['people'] = people

        if (models.Group.objects.filter(person__in=people).exists() and
                instance.group_by_group):
            context['people_groups'] = self.group_people(
                people, instance.language)
            context['group_less_people'] = people.filter(group__isnull=True)
        else:
            context['people_groups'] = []
            context['group_less_people'] = []
        return context

plugin_pool.register_plugin(PeoplePlugin)
