# -*- coding: utf8 -*-
from django.conf.urls import include, url

urlpatterns = [
    url(r'^accounts/', include('nopassword.urls')),
    url(r'^accounts-rest/', include('nopassword.rest.urls')),
]
