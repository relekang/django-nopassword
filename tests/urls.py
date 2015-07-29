# -*- coding: utf8 -*-
from django.conf.urls import include, patterns, url

urlpatterns = patterns(
    '',
    url(r'^accounts/', include('nopassword.urls')),
)
