# -*- coding: utf-8 -*-
from django.contrib import admin

from nopassword import models


@admin.register(models.LoginCode)
class LoginCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'timestamp')
    ordering = ('-timestamp',)
    readonly_fields = ('code', 'user', 'timestamp', 'next')
