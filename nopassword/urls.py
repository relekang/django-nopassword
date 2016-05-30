# -*- coding: utf8 -*-
from django.conf.urls import url
from nopassword.views import login, login_with_code, \
    login_with_code_and_username, logout


urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^login-code/(?P<login_code>[a-zA-Z0-9]+)/$', login_with_code),
    url(r'^login-code/(?P<username>[a-zA-Z0-9_@\.\+-]+)/(?P<login_code>[a-zA-Z0-9]+)/$',
        login_with_code_and_username),
    url(r'^logout/$', logout),
]
