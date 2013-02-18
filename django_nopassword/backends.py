# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django_nopassword.models import LoginCode

#Todo: move to settings
TIMEOUT = timedelta(minutes=15)


class EmailBackend:
    
    def authenticate(self, username, code=None):
        try:
            user = User.objects.get(username=username)
            if code is None:
                return LoginCode.create_code_for_user(user)
            else:
                timestamp = datetime.now() + TIMEOUT
                login_code = LoginCode.objects.get(user=user, code=code, timestamp__lt=timestamp)
                user = login_code.user
                user.code = login_code
                login_code.delete()
                return user
        except (TypeError, User.DoesNotExist):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None