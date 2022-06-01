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
        user = User.objects.create_user(
            validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name'
        )