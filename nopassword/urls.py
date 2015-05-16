# -*- coding: utf8 -*-
from django.conf.urls import url

urlpatterns = [
    url(r'^login/$', 'nopassword.views.login', name='login'),
    url(r'^login-code/(?P<login_code>[a-zA-Z0-9]+)/$',
        'nopassword.views.login_with_code'),
    url(r'^login-code/(?P<username>[a-zA-Z0-9_@\.-]+)/(?P<login_code>[a-zA-Z0-9]+)/$',
        'nopassword.views.login_with_code_and_username'),
    url(r'^logout/$', 'nopassword.views.logout'),
]
