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


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('author', 'name', 'description',
        'ingridients', 'tag', 'time')
        lookup_field = 'author'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('title', 'slug', 'color')
        lookup_field = 'slug'


class IngridientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingridient
        fields = ('title', 'amount', 'unit')
        lookup_field = 'title'