from django.shortcuts import render
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True
    )
    username = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r'^[\w.@+-]'
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r'^[\w.@+-]'
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
            'role',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"'
            )
        return value


class TokenSerializer(serializers.Serializer):
    password = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r'^[\w.@+-]'
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )