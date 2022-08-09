from django.contrib import admin

from django.contrib.admin import register
from recipes.models import Cart, Favorite, Ingredient
from recipes.models import Recipe, Tag

EMPTY = '< Тут Пусто >'
# class IngredientMountInLine(admin.TabularInLine):
#     model = IngredientMount


@register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'cooking_time'
    )
    search_fields = ('name', 'author__username', 'author__email')
    list_filter = ('tags',)
    # inlines = [IngredientMountInLine]


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
        'get_tags'
    )
    search_fields = ('recipe__name',
                     'recipe__author__username',
                     'recipe__author__email',)
    # list_filter = ('get_tags',)
    empty_value_display = EMPTY

    def get_tags(self, obj):
        try:
            return obj.recipe.tags
        except Favorite.recipe.RelatedObjectDoesNotExist:
            return EMPTY


class CartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    search_fields = ('recipe__name',
                     'recipe__author__username',
                     'recipe__author__email',)
    # list_filter = ('tags',)


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color'
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


# admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
