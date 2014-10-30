# -*- coding: utf-8 -*-
import time

from django.contrib.auth import authenticate
from django.http import Http404
from django.test import Client
from django.test import RequestFactory
from django.test.utils import override_settings
from django.utils import unittest
from django.conf import settings
from django.template.loader import render_to_string

from mock import patch, MagicMock

from nopassword import views
from nopassword.models import LoginCode
from nopassword.utils import get_user_model
from nopassword.backends import NoPasswordBackend
from nopassword.backends.sms import TwilioBackend

from .models import NoUsernameUser, PhoneNumberUser


class TestLoginCodes(unittest.TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user')
        self.inactive_user = get_user_model().objects.create(username='inactive', is_active=False)

    def tearDown(self):
        self.user.delete()
        self.inactive_user.delete()

    def test_login_backend(self):
        self.code = LoginCode.create_code_for_user(self.user)
        self.assertEqual(len(self.code.code), 20)
        self.assertIsNotNone(authenticate(username=self.user.username, code=self.code.code))
        self.assertEqual(LoginCode.objects.filter(user=self.user, code=self.code.code).count(), 0)

        authenticate(username=self.user.username)
        self.assertEqual(LoginCode.objects.filter(user=self.user).count(), 1)

        self.assertIsNone(LoginCode.create_code_for_user(self.inactive_user))
        self.assertIsNone(authenticate(username=self.inactive_user.username))

    @override_settings(NOPASSWORD_CODE_LENGTH=8)
    def test_shorter_code(self):
        self.code = LoginCode.create_code_for_user(self.user)
        self.assertEqual(len(self.code.code), 8)

    def test_next_value(self):
        self.code = LoginCode.create_code_for_user(self.user, next='/secrets/')
        self.assertEqual(self.code.next, '/secrets/')

    @override_settings(NOPASSWORD_LOGIN_CODE_TIMEOUT=1)
    def test_code_timeout(self):
        self.timeout_code = LoginCode.create_code_for_user(self.user)
        time.sleep(3)
        self.assertIsNone(authenticate(username=self.user.username, code=self.timeout_code.code))


class AuthenticationBackendTests(unittest.TestCase):
    @override_settings(AUTH_USER_MODULE=NoUsernameUser)
    def test_authenticate_with_custom_user_model(self):
        """When a custom user model is used that doesn't have a field
        called "username" return `None`
        """
        result = authenticate(username='username')
        self.assertIsNone(result)


    @patch('nopassword.backends.sms.TwilioRestClient')
    @override_settings(AUTH_USER_MODEL='tests.PhoneNumberUser',
                       NOPASSWORD_TWILIO_SID="aaaaaaaa", NOPASSWORD_TWILIO_AUTH_TOKEN="bbbbbbbb", DEFAULT_FROM_NUMBER="+15555555")
    def test_twilio_backend(self, mock_object):
        self.user = get_user_model().objects.create(username='twilio_user')
        self.code = LoginCode.create_code_for_user(self.user, next='/secrets/')
        self.assertEqual(len(self.code.code), 20)
        self.assertIsNotNone(authenticate(username=self.user.username, code=self.code.code))
        self.assertEqual(LoginCode.objects.filter(user=self.user, code=self.code.code).count(), 0)

        self.backend = TwilioBackend()
        self.backend.twilio_client.messages.create = MagicMock()

        self.backend.send_login_code(self.code)
        self.assertTrue(mock_object.called)
        self.assertTrue(self.backend.twilio_client.messages.create.called)

        authenticate(username=self.user.username)
        self.assertEqual(LoginCode.objects.filter(user=self.user).count(), 1)

        self.user.delete()



class TestViews(unittest.TestCase):

    def setUp(self):
        self.c = Client()
        self.user = get_user_model().objects.create(username='user')

    def tearDown(self):
        self.user.delete()

    def test_login(self):
        response = self.c.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

        login = self.c.post('/accounts/login/?next=/secret/', {'username': self.user.username})
        self.assertEqual(login.status_code, 200)

        login_with_code = self.c.get('/accounts/login-code/%s/%s/' % (self.user.username,
                                                                      'wrongcode'))
        self.assertEqual(login_with_code.status_code, 404)

        login_url = '/accounts/login-code/%s/%s/' % (
            self.user.username,
            LoginCode.objects.all()[0].code
        )
        login_with_code = self.c.get(login_url)
        self.assertEqual(login_with_code.status_code, 200)

        login_post = self.c.post(login_url)
        self.assertEqual(login_post.status_code, 302)

        logout = self.c.get('/accounts/logout/')
        self.assertEqual(logout.status_code, 302)

    @override_settings(NOPASSWORD_POST_REDIRECT=False)
    def test_login_with_get(self):
        login = self.c.post('/accounts/login/?next=/secret/', {'username': self.user.username})
        self.assertEqual(login.status_code, 200)

        login_url = '/accounts/login-code/%s/%s/' % (
            self.user.username,
            LoginCode.objects.all()[0].code
        )
        login_with_code = self.c.get(login_url)
        self.assertEqual(login_with_code.status_code, 302)

    @override_settings(NOPASSWORD_HIDE_USERNAME=True)
    def test_hide_username(self):
        response = self.c.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

        login = self.c.post('/accounts/login/?next=/secret/', {'username': self.user.username})
        self.assertEqual(login.status_code, 200)

        login_with_code = self.c.get('/accounts/login-code/%s/' % 'wrongcode')
        self.assertEqual(login_with_code.status_code, 404)

        code_url = '/accounts/login-code/%s/' % LoginCode.objects.all()[0].code
        login_with_code = self.c.get(code_url)
        self.assertEqual(login_with_code.status_code, 200)

        login_post = self.c.post(code_url)
        self.assertEqual(login_post.status_code, 302)

        logout = self.c.get('/accounts/logout/')
        self.assertEqual(logout.status_code, 302)


class TestUsersJsonView(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_404(self):
        request = self.factory.get('/accounts/users.json')
        try:
            response = views.users_json(request)
            self.assertEqual(response.status_code, 404)
        except Http404:
            pass

    @override_settings(NOPASSWORD_AUTOCOMPLETE=True)
    def test_200(self):
        request = self.factory.get('/accounts/users.json')
        response = views.users_json(request)
        self.assertEqual(response.status_code, 200)


class TestBackendUtils(unittest.TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user')
        self.inactive_user = get_user_model().objects.create(username='inactive', is_active=False)
        self.backend = NoPasswordBackend()

    def tearDown(self):
        self.user.delete()
        self.inactive_user.delete()

    def test_verify_user(self):
        self.assertTrue(self.backend.verify_user(self.user))
        self.assertFalse(self.backend.verify_user(self.inactive_user))

    def test_send_login_code(self):
        self.assertRaises(NotImplementedError, self.backend.send_login_code)
