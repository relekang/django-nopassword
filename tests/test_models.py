# -*- coding: utf8 -*-
import time

from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase
from django.test.utils import override_settings

from nopassword.models import LoginCode


class TestLoginCodes(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user')
        self.inactive_user = get_user_model().objects.create(username='inactive', is_active=False)
        self.code = LoginCode.create_code_for_user(self.user)

    def tearDown(self):
        self.user.delete()
        self.inactive_user.delete()

    def test_login_backend(self):
        self.assertEqual(len(self.code.code), 20)
        self.assertIsNotNone(authenticate(username=self.user.username, code=self.code.code))
        self.assertEqual(LoginCode.objects.filter(user=self.user, code=self.code.code).count(), 0)
        self.assertIsNone(LoginCode.create_code_for_user(self.inactive_user))

    @override_settings(NOPASSWORD_CODE_LENGTH=8)
    def test_shorter_code(self):
        code = LoginCode.create_code_for_user(self.user)
        self.assertEqual(len(code.code), 8)

    @override_settings(NOPASSWORD_NUMERIC_CODES=True)
    def test_numeric_code(self):
        code = LoginCode.create_code_for_user(self.user)
        self.assertEqual(len(code.code), 20)
        self.assertTrue(code.code.isdigit())

    def test_next_value(self):
        code = LoginCode.create_code_for_user(self.user, next='/secrets/')
        self.assertEqual(code.next, '/secrets/')

    @override_settings(NOPASSWORD_LOGIN_CODE_TIMEOUT=1)
    def test_code_timeout(self):
        timeout_code = LoginCode.create_code_for_user(self.user)
        time.sleep(3)
        self.assertIsNone(authenticate(username=self.user.username, code=timeout_code.code))

    def test_login_url_secure(self):
        self.assertTrue(self.code.login_url(secure=True).startswith('https:'))

    def test_login_url_insecure(self):
        self.assertTrue(self.code.login_url().startswith('http:'))

    def test_login_url_host(self):
        host = 'nopassword.example.com'
        self.assertIn(host, self.code.login_url(host=host))

    @override_settings(SERVER_URL='server_url_setting.example.com')
    def test_login_url_default_setting(self):
        self.assertIn('server_url_setting.example.com', self.code.login_url())

    @override_settings(SERVER_URL=None)
    def test_login_url_no_setting(self):
        self.assertIn('example.com', self.code.login_url())
