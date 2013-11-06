# -*- coding: utf-8 -*-
from collections import defaultdict

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

    def group_people(self, people, language):
        groups = defaultdict(list)

        for people in people:
            groups[people.group].append(people)

        # Python/Django bug ?
        groups.default_factory = None
        return groups

    def render(self, context, instance, placeholder):
        people = instance.people.select_related('group', 'visual')

        context['instance'] = instance
        context['people'] = people

        if models.Group.objects.filter(person__in=people).exists() and instance.group_by_group:
            context['people_groups'] = self.group_people(people, instance.language)
            context['group_less_people'] = people.filter(group__isnull=True)
        else:
            context['people_groups'] = []
            context['group_less_people'] = []
        try:
            reverse('download_vcard', args=(1,))
            context['show_vcard'] = True
        except NoReverseMatch:
            pass
        return context

plugin_pool.register_plugin(PeoplePlugin)