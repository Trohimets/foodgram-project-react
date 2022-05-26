from django.shortcuts import render
from rest_framework import serializers
from recipes.models import Tag, Recipe, Ingridient


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = ('id','tags', 'author','ingridients', 'name', 'description',
                  'time')
        lookup_field = 'author'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        lookup_field = 'slug'


class IngridientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingridient
        fields = ('id', 'name', 'measurement_unit')
        lookup_field = 'name'