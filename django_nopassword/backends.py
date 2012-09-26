# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django_nopassword.models import LoginCode

class EmailBackend:
    
    def authenticate(self, username, password=None):
        try:
            user = User.objects.get(username=username)
            user = LoginCode.check(user, password)
            return user
        except (TypeError, User.DoesNotExist):
            return None
