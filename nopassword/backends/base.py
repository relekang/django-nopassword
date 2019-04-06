# -*- coding: utf-8 -*-
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone

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
            timestamp = timezone.now() - timedelta(seconds=timeout)

            # We don't delete the login code when authenticating,
            # as that is done during validation of the login form
            # and validation should not have any side effects.
            # It is the responsibility of the view/form to delete the token
            # as soon as the login was successful.

            for c in LoginCode.objects.filter(user=user, timestamp__gt=timestamp):
                if c.code == code:
                    user.login_code = c
                    return user
            return

        except (get_user_model().DoesNotExist, LoginCode.DoesNotExist):
            return

    def send_login_code(self, code, context, **kwargs):
        raise NotImplementedError
