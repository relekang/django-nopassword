# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import FieldError

from nopassword.models import LoginCode
from nopassword.utils import get_user_model


class NoPasswordBackend(ModelBackend):
    def authenticate(self, code=None, **credentials):
        try:
            user = get_user_model().objects.get(**credentials)
            if not self.verify_user(user):
                return None
            if code is None:
                return LoginCode.create_code_for_user(user)
            else:
                timeout = getattr(settings, 'NOPASSWORD_LOGIN_CODE_TIMEOUT', 900)
                timestamp = datetime.now() - timedelta(seconds=timeout)
                login_code = LoginCode.objects.get(user=user, code=code, timestamp__gt=timestamp)
                user = login_code.user
                user.code = login_code
                login_code.delete()
                return user
        except (TypeError, get_user_model().DoesNotExist, LoginCode.DoesNotExist, FieldError):
            return None

    def send_login_code(self, code, secure=False, host=None, **kwargs):
        raise NotImplementedError

    def verify_user(self, user):
        return user.is_active
