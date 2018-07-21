# -*- coding: utf8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token

from nopassword.models import LoginCode


class TestRestViews(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='user')

    def test_request_login_code(self):
        response = self.client.post('/accounts-rest/login-code/request/', {
            'username': self.user.username,
        })

        self.assertEqual(response.status_code, 200)

        login_code = LoginCode.objects.filter(user=self.user).first()

        self.assertIsNotNone(login_code)

    def test_request_login_code_missing_username(self):
        response = self.client.post('/accounts-rest/login-code/request/')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'username': ['This field is required.'],
        })

    def test_request_login_code_unknown_user(self):
        response = self.client.post('/accounts-rest/login-code/request/', {
            'username': 'unknown',
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'username': ['Please enter a correct userid. Note that it is case-sensitive.'],
        })

    def test_request_login_code_inactive_user(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post('/accounts-rest/login-code/request/', {
            'username': self.user.username,
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'username': ['This account is inactive.'],
        })

    def test_login(self):
        login_code = LoginCode.objects.create(user=self.user, code='foobar')

        response = self.client.post('/accounts-rest/login/', {
            'code': login_code.code,
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(LoginCode.objects.filter(pk=login_code.pk).exists())

        token = Token.objects.filter(user=self.user).first()

        self.assertIsNotNone(token)
        self.assertEqual(response.data['key'], token.key)

    def test_login_missing_code(self):
        response = self.client.post('/accounts-rest/login/')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'code': ['This field is required.'],
        })

    def test_login_unknown_code(self):
        response = self.client.post('/accounts-rest/login/', {
            'code': 'unknown',
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'code': ['Login code is invalid. It might have expired.'],
        })

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()

        login_code = LoginCode.objects.create(user=self.user, code='foobar')

        response = self.client.post('/accounts-rest/login/', {
            'code': login_code.code,
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'code': ['Unable to log in with provided login code.'],
        })

    def test_logout(self):
        token = Token.objects.create(user=self.user, key='foobar')

        response = self.client.post(
            '/accounts-rest/logout/',
            HTTP_AUTHORIZATION='Token {}'.format(token.key),
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_unknown_token(self):
        login_code = LoginCode.objects.create(user=self.user, code='foobar')

        self.client.login(username=self.user.username, code=login_code.code)

        response = self.client.post(
            '/accounts-rest/logout/',
            HTTP_AUTHORIZATION='Token unknown',
        )

        self.assertEqual(response.status_code, 200)
