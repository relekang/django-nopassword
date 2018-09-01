# -*- coding: utf8 -*-
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory, TestCase, override_settings
from mock import MagicMock

from nopassword import forms


class TestLoginForm(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create(username='user')

    def test_domain_override(self):
        request = self.factory.post('/accounts/login/', {
            'username': 'user',
        })
        form = forms.LoginForm(data=request.POST)
        form.send_login_code = MagicMock()

        self.assertTrue(form.is_valid())

        form.save(request, domain_override='foobar.com')

        self.assertTrue(form.send_login_code.called)
        (login_code, context), _ = form.send_login_code.call_args
        self.assertIn('http://foobar.com', context['url'])

    def test_extra_context(self):
        request = self.factory.post('/accounts/login/', {
            'username': 'user',
        })
        form = forms.LoginForm(data=request.POST)
        form.send_login_code = MagicMock()

        self.assertTrue(form.is_valid())

        form.save(request, extra_context={'foo': 'bar'})

        self.assertTrue(form.send_login_code.called)
        (login_code, context), _ = form.send_login_code.call_args
        self.assertTrue('url' in context)
        self.assertEqual('bar', context['foo'])

    @override_settings(
        AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'],
    )
    def test_missing_backend(self):
        form = forms.LoginForm()
        self.assertRaises(ImproperlyConfigured, form.send_login_code, None, None)
