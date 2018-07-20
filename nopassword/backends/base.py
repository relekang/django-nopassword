# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from nopassword.models import LoginCode


class NoPasswordBackend(ModelBackend):

    def authenticate(self, request, username=None, code=None, **kwargs):
        if username is None:
            username = kwargs.get(get_user_model().USERNAME_FIELD)

        if not username or not code:
            return

        try:
            user = get_user_model()._default_manager.get_by_natural_key(username)

            if not self.user_can_authenticate(user):
                return

            timeout = getattr(settings, 'NOPASSWORD_LOGIN_CODE_TIMEOUT', 900)
            timestamp = datetime.now() - timedelta(seconds=timeout)
            login_code = LoginCode.objects.get(user=user, code=code, timestamp__gt=timestamp)
            user = login_code.user
            user.code = login_code
            login_code.delete()

            return user

        except (get_user_model().DoesNotExist, LoginCode.DoesNotExist):
            return

    def send_login_code(self, code, secure=False, host=None, **kwargs):
        raise NotImplementedError
