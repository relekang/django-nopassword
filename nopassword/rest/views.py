# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from nopassword.rest import serializers


class LoginView(GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": _("Login code has been sent.")},
            status=status.HTTP_200_OK
        )


@method_decorator(sensitive_post_parameters('code'), 'dispatch')
class LoginCodeView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.LoginCodeSerializer
    token_serializer_class = serializers.TokenSerializer
    token_model = Token

    def process_login(self):
        django_login(self.request, self.user)

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token, created = self.token_model.objects.get_or_create(user=self.user)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        token_serializer = self.token_serializer_class(
            instance=self.token,
            context=self.get_serializer_context(),
        )
        data = token_serializer.data
        data['next'] = self.serializer.validated_data['code'].next
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        self.serializer.save()
        self.login()
        return self.get_response()


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        django_logout(request)

        return Response(
            {"detail": _("Successfully logged out.")},
            status=status.HTTP_200_OK,
        )
