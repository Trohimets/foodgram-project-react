from django.shortcuts import render
from rest_framework import serializers
from recipes.models import Tag, Recipe, Ingredient
from users.serializers import RegistrationSerializer

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

# GET Recipe
class RecipeGetSerializer(serializers.ModelSerializer):
    author = RegistrationSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientSerializer(read_only=True, many=True)
    class Meta:
        model = Recipe
        fields = ('id','tags', 'author','ingredients', 'name', 'text',
                  'cooking_time')
        lookup_field = 'author'

# POST Recipe
class RecipePostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientSerializer(read_only=True, many=True)
    class Meta:
        model = Recipe
        fields = ('tags', 'ingredients', 'name', 'text',
                  'cooking_time')
        lookup_field = 'author'