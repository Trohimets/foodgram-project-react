from django.shortcuts import render
from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password
from djoser.serializers import UserCreateSerializer

class RegistrationSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data['password'] = (
            make_password(validated_data.pop('password'))
        )
        return super().create(validated_data)