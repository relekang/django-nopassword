# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.views import login as django_login
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AuthenticationForm
from .models import LoginCode
from .utils import get_username, get_username_field


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            code = LoginCode.objects.filter(**{
                'user__%s' % get_username_field(): request.POST.get('username')
            })[0]
            code.next = request.GET.get('next')
            code.save()
            code.send_login_code(
                secure=request.is_secure(),
                host=request.get_host(),
            )
            return render(request, 'registration/sent_mail.html')

    return django_login(request, authentication_form=AuthenticationForm)


def login_with_code(request, login_code):
    code = get_object_or_404(LoginCode.objects.select_related('user'), code=login_code)
    return login_with_code_and_username(request, username=get_username(code.user),
                                        login_code=login_code)


def login_with_code_and_username(request, username, login_code):
    code = get_object_or_404(LoginCode, code=login_code)
    login_with_post = getattr(settings, 'NOPASSWORD_POST_REDIRECT', True)

    if request.method == 'POST' or not login_with_post:
        user = authenticate(**{get_username_field(): username, 'code': login_code})
        if user is None:
            raise Http404
        user = auth_login(request, user)
        return redirect(code.next)

    return render(request, 'registration/login_submit.html')


def logout(request, redirect_to=None):
    auth_logout(request)
    if redirect_to is None:
        return redirect('{0}:login'.format(getattr(settings, 'NOPASSWORD_NAMESPACE', 'nopassword')))
    else:
        return redirect(redirect_to)
