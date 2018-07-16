# -*- coding: utf-8 -*-
from django.conf.urls import url

from nopassword.rest import views

app_name = 'nopassword'
urlpatterns = [
    url(
        r'^login-code/request/$',
        views.LoginCodeRequestView.as_view(),
        name='rest_login_code_request',
    ),
    url(r'^login/$', views.LoginView.as_view(), name='rest_login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='rest_logout'),
]
