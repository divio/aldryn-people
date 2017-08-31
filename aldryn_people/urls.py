# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from aldryn_people import views
from django.conf.urls import url

urlpatterns = [
    url(r'^group/(?P<pk>[0-9]+)/$',
        views.GroupDetailView.as_view(), name='group-detail'),
    url(r'^group/(?P<slug>[A-Za-z0-9_\-]+)/$',
        views.GroupDetailView.as_view(), name='group-detail'),

    url(r'^(?P<pk>[0-9]+)/$',
        views.PersonDetailView.as_view(), name='person-detail'),
    url(r'^(?P<slug>[A-Za-z0-9_\-]+)/$',
        views.PersonDetailView.as_view(), name='person-detail'),

    url(r'^(?P<pk>[0-9]+)/download/$',
        views.DownloadVcardView.as_view(), name='download_vcard'),
    url(r'^(?P<slug>[A-Za-z0-9_\-]+)/download/$',
        views.DownloadVcardView.as_view(), name='download_vcard'),

    url(r'^$',
        views.GroupListView.as_view(), name='group-list'),
]
