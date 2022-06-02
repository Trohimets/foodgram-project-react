from re import S
from rest_framework import serializers
from recipes.models import (Tag, Recipe,
                            Ingredient, IngredientMount, TagRecipe)
from users.serializers import RegistrationSerializer
from drf_extra_fields.fields import Base64ImageField


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        lookup_field = 'slug'


class BaseIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountGetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientMount
        fields = ('id', 'name', 'measurement_unit', 'amount')

class IngredientAmountPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientMount
        fields = ('id', 'amount')


# GET Recipe
class RecipeGetSerializer(serializers.ModelSerializer):
    author = RegistrationSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientAmountGetSerializer(read_only=True, many=True)
    #is_favorited = serializers.SerializerMethodField()
    #in_shopping_list = serializers.SerializerMethodField()

    
    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 
                  'text', 'cooking_time')
        lookup_field = 'author'
# 'is_favorited', 'in_shopping_list')

# POST Recipe
class RecipePostSerializer(serializers.ModelSerializer):
    author = RegistrationSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)
    ingredients = IngredientAmountPostSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'author', 'name', 'text',
                  'cooking_time')
        lookup_field = 'author'

    def create(self, validated_data):
        tags_set = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags_set:
            TagRecipe.objects.create(
                recipe=recipe,
                tag=tag
            )
        for ingredient in ingredients:
            IngredientMount.objects.create(
                 ingredient=ingredient['id'],
                 recipe=recipe, amount=ingredient['amount'])
        return recipe
