# -*- coding: utf8 -*-
import time

from django.contrib.auth import authenticate
from django.test.utils import override_settings
from django.utils import unittest

from nopassword.models import LoginCode
from nopassword.utils import get_user_model


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

    @override_settings(NOPASSWORD_NUMERIC_CODES=True)
    def test_shorter_code(self):
        self.code = LoginCode.create_code_for_user(self.user)
        self.assertEqual(len(self.code.code), 20)
        self.assertTrue(self.code.code.isdigit())

    def test_next_value(self):
        self.code = LoginCode.create_code_for_user(self.user, next='/secrets/')
        self.assertEqual(self.code.next, '/secrets/')

    @override_settings(NOPASSWORD_LOGIN_CODE_TIMEOUT=1)
    def test_code_timeout(self):
        self.timeout_code = LoginCode.create_code_for_user(self.user)
        time.sleep(3)
        self.assertIsNone(authenticate(username=self.user.username, code=self.timeout_code.code))
