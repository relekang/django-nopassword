# -*- coding: utf-8 -*-
import json
from django.contrib.auth.views import login as django_login
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django_nopassword.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django_nopassword.utils import User


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return render(request, 'registration/sent_mail.html')

    return django_login(request, authentication_form=AuthenticationForm)


def login_with_code(request, username, login_code):
    user = authenticate(username=username, code=login_code)

    if user is None:
        raise Http404

    elif not user.pk:
        raise Http404

    next = request.GET.get('next')
    user = auth_login(request, user)

    return redirect(next)


def logout(request, redirect_to=None):
    auth_logout(request)
    if redirect_to is None:
        return redirect(reverse('login'))

    else:
        return redirect(redirect_to)


def users_json(request):
    users = []
    for user in User.objects.filter(is_active=True):
        users.append({
            'value': user.username,
            'username': user.username,
            'full_name': user.get_full_name(),
        })

    return HttpResponse(json.dumps(users))