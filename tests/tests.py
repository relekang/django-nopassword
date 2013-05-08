# -*- coding: utf8 -*-
import time

from django.contrib.auth import authenticate
from django.test.utils import override_settings
from django.utils import unittest

from django_nopassword.models import LoginCode
from django_nopassword.utils import User


class TestLoginCodes(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.inactive_user = User.objects.create(username='inactive', is_active=False)

    def test_login_backend(self):
        self.code = LoginCode.create_code_for_user(self.user)
        self.assertEqual(len(self.code.code), 20)
        self.assertIsNotNone(authenticate(username=self.user.username, code=self.code.code))
        self.assertEqual(LoginCode.objects.filter(user=self.user, code=self.code.code).count(), 0)

        self.assertIsNone(LoginCode.create_code_for_user(self.inactive_user))

    @override_settings(LOGIN_CODE_TIMEOUT=1)
    def test_code_timeout(self):
        self.timeout_code = LoginCode.create_code_for_user(self.user)
        time.sleep(3)
        self.assertIsNone(authenticate(username=self.user.username, code=self.timeout_code.code))

    def tearDown(self):
        self.user.delete()
        self.inactive_user.delete()
