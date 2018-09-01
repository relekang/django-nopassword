# -*- coding: utf8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from nopassword.models import LoginCode


class TestViews(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='user')

    def test_request_login_code(self):
        response = self.client.post('/accounts/login/', {
            'username': self.user.username,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/accounts/login/code/')

        login_code = LoginCode.objects.filter(user=self.user).first()

        self.assertIsNotNone(login_code)

    def test_request_login_code_missing_username(self):
        response = self.client.post('/accounts/login/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {
            'username': ['This field is required.'],
        })

    def test_request_login_code_unknown_user(self):
        response = self.client.post('/accounts/login/', {
            'username': 'unknown',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {
            'username': ['Please enter a correct userid. Note that it is case-sensitive.'],
        })

    def test_request_login_code_inactive_user(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post('/accounts/login/', {
            'username': self.user.username,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {
            'username': ['This account is inactive.'],
        })

    def test_login_post(self):
        login_code = LoginCode.objects.create(user=self.user, code='foobar')

        response = self.client.post('/accounts/login/code/', {
            'code': login_code.code,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/accounts/profile/')
        self.assertEqual(response.wsgi_request.user, self.user)
        self.assertFalse(LoginCode.objects.filter(pk=login_code.pk).exists())

    def test_login_get(self):
        login_code = LoginCode.objects.create(user=self.user, code='foobar')

        response = self.client.get('/accounts/login/code/', {
            'code': login_code.code,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].cleaned_data['code'], login_code)
        self.assertTrue(response.wsgi_request.user.is_anonymous)
        self.assertTrue(LoginCode.objects.filter(pk=login_code.pk).exists())

    @override_settings(NOPASSWORD_LOGIN_ON_GET=True)
    def test_login_get_non_idempotent(self):
        login_code = LoginCode.objects.create(user=self.user, code='foobar')

        response = self.client.get('/accounts/login/code/', {
            'code': login_code.code,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/accounts/profile/')
        self.assertEqual(response.wsgi_request.user, self.user)
        self.assertFalse(LoginCode.objects.filter(pk=login_code.pk).exists())

    def test_login_missing_code_post(self):
        response = self.client.post('/accounts/login/code/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {
            'code': ['This field is required.'],
        })

    def test_login_missing_code_get(self):
        response = self.client.get('/accounts/login/code/')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_bound)

    def test_login_unknown_code(self):
        response = self.client.post('/accounts/login/code/', {
            'code': 'unknown',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {
            'code': ['Login code is invalid. It might have expired.'],
        })

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()

        login_code = LoginCode.objects.create(user=self.user, code='foobar')

        response = self.client.post('/accounts/login/code/', {
            'code': login_code.code,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {
            'code': ['Unable to log in with provided login code.'],
        })

    def test_logout_post(self):
        login_code = LoginCode.objects.create(user=self.user, code='foobar')

        self.client.login(username=self.user.username, code=login_code.code)

        response = self.client.post('/accounts/logout/?next=/accounts/login/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/accounts/login/')
        self.assertTrue(response.wsgi_request.user.is_anonymous)

    def test_logout_get(self):
        login_code = LoginCode.objects.create(user=self.user, code='foobar')

        self.client.login(username=self.user.username, code=login_code.code)

        response = self.client.post('/accounts/logout/?next=/accounts/login/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/accounts/login/')
        self.assertTrue(response.wsgi_request.user.is_anonymous)
