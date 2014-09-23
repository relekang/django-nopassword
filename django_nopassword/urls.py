# -*- coding: utf8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^login/$', 'django_nopassword.views.login', name='login'),
    url(r'^login-code/(?P<login_code>[a-zA-Z0-9]+)/$',
        'django_nopassword.views.login_with_code'),
    url(r'^login-code/(?P<username>[a-zA-Z0-9_@\.-]+)/(?P<login_code>[a-zA-Z0-9]+)/$',
        'django_nopassword.views.login_with_code_and_username'),
    url(r'^logout/$', 'django_nopassword.views.logout'),
    url(r'^users.json$', 'django_nopassword.views.users_json'),
)
