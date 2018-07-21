# -*- coding: utf8 -*-
import time
from datetime import datetime

from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase
from django.test.utils import override_settings

from nopassword.models import LoginCode


class TestLoginCodes(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user')
        self.inactive_user = get_user_model().objects.create(username='inactive', is_active=False)
        self.code = LoginCode.create_code_for_user(self.user)

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

    def test_str(self):
        code = LoginCode(user=self.user, code='foo', timestamp=datetime(2018, 7, 1))
        self.assertEqual(str(code), 'test_user - 2018-07-01 00:00:00')
