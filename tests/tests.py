# -*- coding: utf8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import unittest

from django_nopassword.models import LoginCode


class TestLoginCodes(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')

    def test_login_backend(self):
        self.code = LoginCode.create_code_for_user(self.user)
        self.assertEqual(len(self.code.code), 20)
        self.assertIsNotNone(authenticate(username=self.user.username, code=self.code.code))
        self.assertEqual(LoginCode.objects.filter(user=self.user, code=self.code.code).count(), 0)

    def tearDown(self):
        self.user.delete()
