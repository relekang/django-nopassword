# -*- coding: utf8 -*-
import time

from django.contrib.auth import authenticate
from django.test import Client
from django.test.utils import override_settings
from django.utils import unittest
from django_nopassword import views

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

        authenticate(username=self.user.username)
        self.assertEqual(LoginCode.objects.filter(user=self.user).count(), 1)

        self.assertIsNone(LoginCode.create_code_for_user(self.inactive_user))
        self.assertIsNone(authenticate(username=self.inactive_user.username))

    def test_next_value(self):
        self.code = LoginCode.create_code_for_user(self.user, next='/secrets/')
        self.assertEqual(self.code.next, '/secrets/')

    @override_settings(NOPASSWORD_LOGIN_CODE_TIMEOUT=1)
    def test_code_timeout(self):
        self.timeout_code = LoginCode.create_code_for_user(self.user)
        time.sleep(3)
        self.assertIsNone(authenticate(username=self.user.username, code=self.timeout_code.code))

    def tearDown(self):
        self.user.delete()
        self.inactive_user.delete()


class TestViews(unittest.TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create(username='user')

    def test_login(self):
        response = self.c.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

        login = self.c.post('/accounts/login/?next=/secret/', {'username': self.user.username})
        self.assertEqual(login.status_code, 200)

        login_with_code = self.c.get('/accounts/login-code/%s/%s/' % (self.user.username, 'wrongcode'))
        self.assertEqual(login_with_code.status_code, 404)

        login_with_code = self.c.get('/accounts/login-code/%s/%s/' % (self.user.username, LoginCode.objects.all()[0].code))
        self.assertEqual(login_with_code.status_code, 302)

        logout = self.c.get('/accounts/logout/')
        self.assertEqual(logout.status_code, 302)

    def tearDown(self):
        self.user.delete()