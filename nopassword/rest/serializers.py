# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from nopassword import forms


class LoginCodeRequestSerializer(serializers.Serializer):
    username = serializers.CharField()

    form_class = forms.LoginCodeRequestForm

    def validate(self, data):
        self.form = self.form_class(data=self.initial_data)

        if not self.form.is_valid():
            raise serializers.ValidationError(self.form.errors)

        return self.form.cleaned_data

    def save(self):
        request = self.context.get('request')
        self.form.save(request=request)


class LoginSerializer(serializers.Serializer):
    code = serializers.CharField()

    form_class = forms.LoginForm

    def validate(self, data):
        request = self.context.get('request')

        self.form = self.form_class(data=self.initial_data, request=request)

        if not self.form.is_valid():
            raise serializers.ValidationError(self.form.errors)

        return self.form.cleaned_data


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key',)
