# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string
from twilio.rest import TwilioRestClient

from nopassword.backends.base import NoPasswordBackend


class TwilioBackend(NoPasswordBackend):
    template_name = 'registration/login_code_request_sms.txt'
    from_number = None

    def __init__(self):
        self.twilio_client = TwilioRestClient(
            settings.NOPASSWORD_TWILIO_SID,
            settings.NOPASSWORD_TWILIO_AUTH_TOKEN
        )
        super(TwilioBackend, self).__init__()

    def send_login_code(self, code, context, **kwargs):
        """
        Send a login code via SMS
        """
        from_number = self.from_number or getattr(settings, 'DEFAULT_FROM_NUMBER')
        sms_content = render_to_string('registration/login_sms.txt', context)

        self.twilio_client.messages.create(
            to=code.user.phone_number,
            from_=from_number,
            body=sms_content
        )
