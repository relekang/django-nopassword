# -*- coding: utf8 -*-
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('nopassword.urls')),
    url(r'^accounts-rest/', include('nopassword.rest.urls')),
]
