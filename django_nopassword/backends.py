# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import FieldError
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from .utils import get_user_model
from .models import LoginCode


class NoPasswordBackend:

    supports_inactive_user = True

    def authenticate(self, code=None, **credentials):
        try:
            user = get_user_model().objects.get(**credentials)
            if not user.is_active:
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

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None

    def send_login_code(self):
        raise NotImplementedError


class EmailBackend(NoPasswordBackend):

    def send_login_code(self, code):
        subject = getattr(settings, 'NOPASSWORD_LOGIN_EMAIL_SUBJECT', _('Login code'))
        to_email = [code.user.email]
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'root@example.com')

        context = {'url': code.login_url(), 'code': code}
        text_content = render_to_string('registration/login_email.txt', context)
        html_content = render_to_string('registration/login_email.html', context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
