# -*- coding: utf8 -*-
from django.conf.urls import include, url

urlpatterns = [
    url(r'^accounts/', include('nopassword.urls', namespace='nopassword')),
    url(r'^accounts-rest/', include('nopassword.rest.urls', namespace='nopassword_rest')),
]
