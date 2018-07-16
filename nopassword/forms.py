# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from .utils import get_username_field


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username logins.
    """
    username = forms.CharField(label=_("Username"), max_length=30)

    error_messages = {
        'invalid_login': _("Please enter a correct username. "
                           "Note that it is case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.login_code = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = _(get_username_field().capitalize())

    def clean_username(self):
        username = self.cleaned_data['username']

        self.login_code = authenticate(**{get_username_field(): username})

        if self.login_code is None:
            raise forms.ValidationError(self.error_messages['invalid_login'])

        return username

    def clean(self):
        self.check_for_test_cookie()

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def save(self, request):
        self.login_code.next = request.GET.get('next')
        self.login_code.save()
        self.login_code.send_login_code(secure=request.is_secure(), host=request.get_host())
