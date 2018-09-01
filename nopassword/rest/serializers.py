# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from nopassword import forms


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    next = serializers.CharField(required=False, allow_null=True)

    form_class = forms.LoginForm

    def validate(self, data):
        self.form = self.form_class(data=self.initial_data)

        if not self.form.is_valid():
            raise serializers.ValidationError(self.form.errors)

        return self.form.cleaned_data

    def save(self):
        request = self.context.get('request')
        return self.form.save(request=request)


class LoginCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

    form_class = forms.LoginCodeForm

    def validate(self, data):
        request = self.context.get('request')

        self.form = self.form_class(data=self.initial_data, request=request)

        if not self.form.is_valid():
            raise serializers.ValidationError(self.form.errors)

        return self.form.cleaned_data

    def save(self):
        self.form.save()


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key',)
