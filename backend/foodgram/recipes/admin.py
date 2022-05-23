from django.contrib import admin
from recipes.models import Recipe, Tag, Ingridient
from users.models import User


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'time'
    )
    list_filter = ('author', 'name'
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'color'
    )


class IngridientAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'unit'
    )
    list_filter = ('title',)


class UserADmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'role',
        'email'
    )
    list_filter = ('first_name', 'email')


admin.site.register(User)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingridient, IngridientAdmin)
