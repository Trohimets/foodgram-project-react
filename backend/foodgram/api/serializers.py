from django.shortcuts import render
from rest_framework import serializers
from recipes.models import Tag, Recipe, Ingredient


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        lookup_field = 'slug'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        lookup_field = 'name'


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientSerializer(read_only=True, many=True)
    class Meta:
        model = Recipe
        fields = ('id','tags', 'author','ingredients', 'name', 'text',
                  'cooking_time')
        lookup_field = 'author'
