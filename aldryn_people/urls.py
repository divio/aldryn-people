# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from aldryn_people.views import DownloadVcardView

urlpatterns = patterns('',
    url(r'^(?P<pk>[0-9]+)/$', DownloadVcardView.as_view(),
        name='download_vcard')
)