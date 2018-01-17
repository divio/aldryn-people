# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from djangocms_helper.urls import urlpatterns


urlpatterns += [
    url(r'^people/', include('aldryn_people.urls', namespace='aldryn_people')),
]
