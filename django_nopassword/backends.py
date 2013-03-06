# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.conf import settings

from django_nopassword.utils import User
from django_nopassword.models import LoginCode


class EmailBackend:
    
    def authenticate(self, username, code=None):
        try:
            user = User.objects.get(username=username)
            if code is None:
                return LoginCode.create_code_for_user(user)
            else:
                timestamp = datetime.now() - timedelta(seconds=getattr(settings, 'LOGIN_CODE_TIMEOUT', 900))
                login_code = LoginCode.objects.get(user=user, code=code, timestamp__gt=timestamp)
                user = login_code.user
                user.code = login_code
                login_code.delete()
                return user
        except (TypeError, User.DoesNotExist, LoginCode.DoesNotExist):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None