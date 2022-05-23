from django.shortcuts import render
from rest_framework import serializers
from recipes.models import User, Tag, Recipe, Ingridient


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'role',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"'
            )
        return value


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=254,
        required=True
    )
    username = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r'^[\w.@+-]'
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r'^[\w.@+-]'
    )
    confirmation_code = serializers.CharField(required=True)


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = ('author', 'name', 'description',
                  'ingridients', 'tags', 'time')
        lookup_field = 'author'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('title', 'slug', 'color')
        lookup_field = 'slug'


class IngridientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingridient
        fields = ('title', 'unit')
        lookup_field = 'title'