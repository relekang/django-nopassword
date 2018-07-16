# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.authtoken.models import Token

from nopassword.forms import AuthenticationForm
from nopassword.models import LoginCode
from nopassword.utils import get_username, get_username_field


class LoginCodeRequestSerializer(serializers.Serializer):
    username = serializers.CharField(label=_('Username'), max_length=30)

    login_code_request_form_class = AuthenticationForm

    def validate(self, data):
        username = data.get('username')

        if username:
            self.login_code_request_form = self.login_code_request_form_class(
                data=self.initial_data,
            )

            if not self.login_code_request_form.is_valid():
                raise serializers.ValidationError(self.login_code_request_form.errors)

        return data

    def save(self):
        request = self.context.get('request')
        self.login_code_request_form.save(request=request)


class LoginSerializer(serializers.Serializer):
    code = serializers.SlugRelatedField(
        label=_('Login code'),
        queryset=LoginCode.objects.select_related('user'),
        slug_field='code',
        style={'base_template': 'input.html'},
    )

    def validate(self, data):
        code = data.get('code')

        if code:
            username = get_username(code.user)
            user = authenticate(**{get_username_field(): username, 'code': code.code})

            if not user:
                raise exceptions.ValidationError({
                    'code': _('Unable to log in with provided credentials.'),
                })

            data['user'] = user

        return data


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key',)
