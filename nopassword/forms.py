# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate, get_backends, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _

from nopassword import models


class LoginForm(forms.Form):
    error_messages = {
        'invalid_username': _(
            "Please enter a correct %(username)s. "
            "Note that it is case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    next = forms.CharField(max_length=200, required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.username_field = get_user_model()._meta.get_field(get_user_model().USERNAME_FIELD)
        self.fields['username'] = self.username_field.formfield()

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            user = get_user_model()._default_manager.get_by_natural_key(username)
        except get_user_model().DoesNotExist:
            raise forms.ValidationError(
                self.error_messages['invalid_username'],
                code='invalid_username',
                params={'username': self.username_field.verbose_name},
            )

        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

        self.cleaned_data['user'] = user

        return username

    def save(self, request, login_code_url='login_code', domain_override=None, extra_context=None):
        login_code = models.LoginCode.create_code_for_user(
            user=self.cleaned_data['user'],
            next=self.cleaned_data['next'],
        )

        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override

        url = '{}://{}{}?code={}'.format(
            'https' if request.is_secure() else 'http',
            domain,
            resolve_url(login_code_url),
            login_code.code,
        )

        context = {
            'domain': domain,
            'site_name': site_name,
            'code': login_code.code,
            'url': url,
        }

        if extra_context:
            context.update(extra_context)

        self.send_login_code(login_code, context)

        return login_code

    def send_login_code(self, login_code, context, **kwargs):
        for backend in get_backends():
            if hasattr(backend, 'send_login_code'):
                backend.send_login_code(login_code, context, **kwargs)
                break
        else:
            raise ImproperlyConfigured(
                'Please add a nopassword authentication backend to settings, '
                'e.g. `nopassword.backends.EmailBackend`'
            )


class LoginCodeForm(forms.Form):
    code = forms.ModelChoiceField(
        label=_('Login code'),
        queryset=models.LoginCode.objects.select_related('user'),
        to_field_name='code',
        widget=forms.TextInput,
        error_messages={
            'invalid_choice': _('Login code is invalid. It might have expired.'),
        },
    )

    error_messages = {
        'invalid_code': _("Unable to log in with provided login code."),
    }

    def __init__(self, request=None, *args, **kwargs):
        super(LoginCodeForm, self).__init__(*args, **kwargs)

        self.request = request

    def clean_code(self):
        code = self.cleaned_data['code']
        username = code.user.get_username()
        user = authenticate(self.request, **{
            get_user_model().USERNAME_FIELD: username,
            'code': code.code,
        })

        if not user:
            raise forms.ValidationError(
                self.error_messages['invalid_code'],
                code='invalid_code',
            )

        self.cleaned_data['user'] = user

        return code

    def get_user(self):
        return self.cleaned_data.get('user')

    def save(self):
        self.cleaned_data['code'].delete()
