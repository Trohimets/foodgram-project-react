from django.shortcuts import render
from rest_framework import serializers
from backend.foodgram.recipes.models import TagRecipe
from recipes.models import Tag, Recipe, Ingredient
from users.serializers import RegistrationSerializer
from django.shortcuts import get_object_or_404


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
    author = RegistrationSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'ingredients', 'name', 'text',
                  'cooking_time')
        lookup_field = 'author'

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            current_tag, status = get_object_or_404(Tag, id=id)
            TagRecipe.objects.create(
                tag=current_tag, recipe=recipe)
        