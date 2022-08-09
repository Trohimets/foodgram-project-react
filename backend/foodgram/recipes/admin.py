from django.contrib import admin

from django.contrib.admin import register
from recipes.models import Cart, Favorite, Ingredient
from recipes.models import Recipe, Tag, IngredientMount

EMPTY = '< Тут Пусто >'


class IngredientInLine(admin.TabularInline):
    model = IngredientMount
    raw_id_fields = ['ingredient']


@register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'cooking_time'
    )
    search_fields = ('name', 'author__username', 'author__email')
    list_filter = ('tags',)
    inlines = [IngredientInLine]


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    search_fields = ('recipe__name',
                     'recipe__author__username',
                     'recipe__author__email',)
    list_filter = ('recipe__tags',)


class CartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    search_fields = ('recipe__name',
                     'recipe__author__username',
                     'recipe__author__email',)
    list_filter = ('recipe__tags',)


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
