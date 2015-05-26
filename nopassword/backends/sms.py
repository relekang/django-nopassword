# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string
from twilio.rest import TwilioRestClient

from .base import NoPasswordBackend


class TwilioBackend(NoPasswordBackend):
    def __init__(self):
        self.twilio_client = TwilioRestClient(
            settings.NOPASSWORD_TWILIO_SID,
            settings.NOPASSWORD_TWILIO_AUTH_TOKEN
        )
        super(TwilioBackend, self).__init__()

    def send_login_code(self, code, secure=False, host=None, **kwargs):
        """
        Send a login code via SMS
        """
        from_number = getattr(settings, 'DEFAULT_FROM_NUMBER')

        context = {'url': code.login_url(secure=secure, host=host), 'code': code}
        sms_content = render_to_string('registration/login_sms.txt', context)

        self.twilio_client.messages.create(
            to=code.user.phone_number,
            from_=from_number,
            body=sms_content
        )
