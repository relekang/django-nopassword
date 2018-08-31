# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView

from nopassword import forms


class LoginCodeRequestView(FormView):
    form_class = forms.LoginCodeRequestForm
    success_url = reverse_lazy('login')
    template_name = 'registration/login_code_request_form.html'

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginCodeRequestView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(request=self.request)
        return super(LoginCodeRequestView, self).form_valid(form)


class LoginView(DjangoLoginView):
    form_class = forms.LoginForm

    def get(self, request, *args, **kwargs):
        if 'code' in self.request.GET and getattr(settings, 'NOPASSWORD_LOGIN_ON_GET', False):
            return super(LoginView, self).post(request, *args, **kwargs)
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super(LoginView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()

        if self.request.method == 'GET' and 'code' in self.request.GET:
            kwargs['data'] = self.request.GET

        return kwargs

    def get_redirect_url(self):
        login_code = getattr(self.request.user, 'login_code', None)
        return login_code.next if login_code else ''


class LogoutView(DjangoLogoutView):
    pass
