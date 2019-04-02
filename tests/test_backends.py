# -*- coding: utf8 -*-
from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase
from django.test.utils import mail, override_settings
from mock import MagicMock, patch

from nopassword.backends.base import NoPasswordBackend
from nopassword.backends.email import EmailBackend
from nopassword.backends.sms import TwilioBackend
from nopassword.models import LoginCode


class AuthenticationBackendTests(TestCase):

    @override_settings(AUTH_USER_MODULE='tests.NoUsernameUser')
    def test_authenticate_with_custom_user_model(self):
        """When a custom user model is used that doesn't have a field
        called "username" return `None`
        """
        result = authenticate(username='username')
        self.assertIsNone(result)


@override_settings(AUTH_USER_MODEL='tests.PhoneNumberUser', NOPASSWORD_TWILIO_SID="aaaaaaaa",
                   NOPASSWORD_TWILIO_AUTH_TOKEN="bbbbbbbb", DEFAULT_FROM_NUMBER="+15555555")
class TwilioBackendTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='twilio_user')
        self.code = LoginCode.create_code_for_user(self.user, next='/secrets/')
        self.assertEqual(len(self.code.code), 64)
        self.assertIsNotNone(authenticate(username=self.user.username, code=self.code.code))

    @patch('nopassword.backends.sms.TwilioRestClient')
    def test_twilio_backend(self, mock_object):
        self.backend = TwilioBackend()
        self.backend.twilio_client.messages.create = MagicMock()
        self.backend.send_login_code(self.code, {'url': 'https://example.com'})
        self.assertTrue(mock_object.called)
        self.assertTrue(self.backend.twilio_client.messages.create.called)
        _, kwargs = self.backend.twilio_client.messages.create.call_args
        self.assertIn('https://example.com', kwargs.get('body'))


class EmailBackendTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='email_user',
            email='nopassword@example.com',
        )
        self.code = LoginCode.create_code_for_user(self.user, next='/secrets/')
        self.backend = EmailBackend()

    def test_email_backend(self):
        "Send email via EmailBackend with default options"
        self.backend.send_login_code(self.code, {'url': 'https://example.com'})
        self.assertEqual(1, len(mail.outbox))
        message = mail.outbox[0]
        self.assertIn('https://example.com', message.body)
        self.assertEqual([self.user.email], message.to)
        self.assertEqual(0, len(message.alternatives))

    def test_html_template_name(self):
        # We don't have an existing html template, so we just use the txt template
        self.backend.html_template_name = 'registration/login_email.txt'
        self.backend.send_login_code(self.code, {'url': 'https://example.com'})
        self.assertEqual(1, len(mail.outbox))
        message = mail.outbox[0]
        self.assertIn('https://example.com', message.body)
        self.assertEqual(1, len(message.alternatives))
        self.assertIn('https://example.com', message.alternatives[0][0])


class TestBackendUtils(TestCase):

    def test_send_login_code(self):
        backend = NoPasswordBackend()
        self.assertRaises(NotImplementedError, backend.send_login_code, code=None, context=None)
