# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.authtoken.models import Token

from nopassword.forms import AuthenticationForm
from nopassword.models import LoginCode


class LoginCodeRequestSerializer(serializers.Serializer):
    username = serializers.CharField()

    login_code_request_form_class = AuthenticationForm

    def __init__(self, *args, **kwargs):
        super(LoginCodeRequestSerializer, self).__init__(*args, **kwargs)
        self.username_field = get_user_model()._meta.get_field(get_user_model().USERNAME_FIELD)
        self.fields['username'].max_length = self.username_field.max_length or 254

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
            username = code.user.get_username()
            user = authenticate(**{get_user_model().USERNAME_FIELD: username, 'code': code.code})

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
