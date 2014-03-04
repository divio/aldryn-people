# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from aldryn_people.views import PersonView, DownloadVcardView

urlpatterns = patterns('',
    url(r'^(?P<pk>[0-9]+)/$', PersonView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/download/$', DownloadVcardView.as_view(), name='download_vcard'),
)