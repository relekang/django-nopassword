# -*- coding: utf-8 -*-
import django

if django.VERSION >= (1, 5):
    from django.contrib.auth import get_user_model
    User = get_user_model()
else:
    from django.contrib.auth.models import User


USERNAME_FIELD = getattr(User, 'USERNAME_FIELD', 'username')


def get_username(user):
    try:
        return user.get_username()
    except AttributeError:
        return user.username
