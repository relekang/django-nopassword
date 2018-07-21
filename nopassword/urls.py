# -*- coding: utf8 -*-
from django.conf.urls import url

from nopassword import views

urlpatterns = [
    url(
        r'^login-code/request/$',
        views.LoginCodeRequestView.as_view(),
        name='login_code_request',
    ),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]
