# -*- coding: utf8 -*-
from mock import patch

from django.utils import unittest
from django.http import Http404
from django.contrib.auth import SESSION_KEY
from django.test import RequestFactory, Client
from django.test.utils import override_settings

from nopassword import views
from nopassword.models import LoginCode
from nopassword.utils import get_user_model


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
        self.assertIn(SESSION_KEY, self.c.session)

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
        self.assertIn(SESSION_KEY, self.c.session)

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

    @patch.object(LoginCode, 'send_login_code')
    def test_https_request(self, mock_send_login_code):
        login = self.c.post('/accounts/login/?next=/secret/', {'username': self.user.username}, **{'wsgi.url_scheme': 'https'})
        self.assertEqual(login.status_code, 200)
        mock_send_login_code.assert_called_with(secure=True)

    @patch.object(LoginCode, 'send_login_code')
    def test_http_request(self, mock_send_login_code):
        login = self.c.post('/accounts/login/?next=/secret/', {'username': self.user.username}, **{'wsgi.url_scheme': 'http'})
        self.assertEqual(login.status_code, 200)
        mock_send_login_code.assert_called_with(secure=False)


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
