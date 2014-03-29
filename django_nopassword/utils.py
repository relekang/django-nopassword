# -*- coding: utf-8 -*-
import django
from django.conf import settings

if django.VERSION >= (1, 5):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    AUTH_USER_MODULE = settings.AUTH_USER_MODULE
else:
    from django.contrib.auth.models import User
    AUTH_USER_MODULE = 'auth.User'


USERNAME_FIELD = getattr(User, 'USERNAME_FIELD', 'username')


def get_username(user):
    try:
        return user.get_username()
    except AttributeError:
        return user.username
