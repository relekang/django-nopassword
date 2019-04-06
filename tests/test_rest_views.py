# -*- coding: utf8 -*-
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from rest_framework.authtoken.models import Token

from nopassword.models import LoginCode


class TestRestViews(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='user', email='foo@bar.com')

    def test_request_login_code(self):
        response = self.client.post('/accounts-rest/login/', {
            'username': self.user.username,
            'next': '/private/',
        })

        self.assertEqual(response.status_code, 200)

        login_code = LoginCode.objects.filter(user=self.user).first()

        self.assertIsNotNone(login_code)
        self.assertEqual(login_code.next, '/private/')
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            'http://testserver/accounts/login/code/?user={}&code={}'.format(
                login_code.user.pk,
                login_code.code
            ),
            mail.outbox[0].body,
        )

    def test_request_login_code_missing_username(self):
        response = self.client.post('/accounts-rest/login/')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'username': ['This field is required.'],
        })

    def test_request_login_code_unknown_user(self):
        response = self.client.post('/accounts-rest/login/', {
            'username': 'unknown',
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'username': ['Please enter a correct userid. Note that it is case-sensitive.'],
        })

    def test_request_login_code_inactive_user(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post('/accounts-rest/login/', {
            'username': self.user.username,
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'username': ['This account is inactive.'],
        })

    def test_login(self):
        login_code = LoginCode.objects.create(user=self.user, next='/private/')

        response = self.client.post('/accounts-rest/login/code/', {
            'user': login_code.user.pk,
            'code': login_code.code,
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(LoginCode.objects.filter(pk=login_code.pk).exists())

        token = Token.objects.filter(user=self.user).first()

        self.assertIsNotNone(token)
        self.assertEqual(response.data, {
            'key': token.key,
            'next': '/private/',
        })

    def test_login_missing_code(self):
        response = self.client.post('/accounts-rest/login/code/')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'code': ['This field is required.'],
        })

    def test_login_unknown_code(self):
        response = self.client.post('/accounts-rest/login/code/', {
            'code': 'unknown',
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            '__all__': ['Unable to log in with provided login code.'],
            'user': ['This field is required.']
        })

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()

        login_code = LoginCode.objects.create(user=self.user)

        response = self.client.post('/accounts-rest/login/code/', {
            'code': login_code.code,
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            '__all__': ['Unable to log in with provided login code.'],
            'user': ['This field is required.']
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
        login_code = LoginCode.objects.create(user=self.user)

        self.client.login(username=self.user.username, code=login_code.code)

        response = self.client.post(
            '/accounts-rest/logout/',
            HTTP_AUTHORIZATION='Token unknown',
        )

        self.assertEqual(response.status_code, 200)
