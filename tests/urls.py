# -*- coding: utf8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^accounts/login/$', 'django_nopassword.views.login'),
    url(r'^accounts/login-code/(?P<username>[a-zA-Z0-9_@\.-]+)/(?P<login_code>[a-zA-Z0-9]+)/$', 'django_nopassword.views.login_with_code'),
    url(r'^accounts/logout/$', 'django_nopassword.views.logout'),
)