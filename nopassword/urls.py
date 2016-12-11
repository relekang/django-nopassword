# -*- coding: utf8 -*-
from django.conf.urls import url

from nopassword import views

urlpatterns = [
    url(
        r'^login/$',
        views.login,
        name='login'
    ),
    url(
        r'^login-code/(?P<login_code>[a-zA-Z0-9]+)/$',
        views.login_with_code,
        name='login_with_code'
    ),
    url(
        r'^login-code/(?P<username>[a-zA-Z0-9_@\.\+-]+)/(?P<login_code>[a-zA-Z0-9]+)/$',
        views.login_with_code_and_username,
        name='login_with_code_and_username'
    ),
    url(
        r'^logout/$',
        views.logout,
        name='logout'
    ),
]
