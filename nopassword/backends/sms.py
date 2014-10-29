from django.conf import settings
from django.core import checks
from nopassword.backends import NoPasswordBackend

from twilio.rest import TwilioRestClient


class SMSBackend(NoPasswordBackend):
    def __init__(self, *args, **kwargs):
        self.twilio_client = TwilioRestClient(settings.NOPASSWORD_TWILIO_SID, settings.NOPASSWORD_TWILIO_AUTH_TOKEN)
        super(SMSBackend, self).__init__(*args, **kwargs)

    def send_login_code(self, code):
        """
        Send a login code via SMS
        """
        from_number = getattr(settings, 'DEFAULT_FROM_NUMBER')

        context = {'url': code.login_url(), 'code': code}
        sms_content = render_to_string('registration/login_sms.txt', context)

        self.client.message.create(to=code.user.phone_number, from=from_number, body=sms_content)
