from django.contrib import admin
from recipes.models import User, Recipe, Tag, Ingridient


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'description',
        'time'
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'color'
    )


class IngridientAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'amount',
        'unit'
    )


admin.site.register(User)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingridient, IngridientAdmin)
