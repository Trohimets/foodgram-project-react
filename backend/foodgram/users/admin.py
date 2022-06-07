from django.contrib import admin

from users.models import Subscribe, User


class UserADmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email'
    )
    list_filter = ('first_name', 'email')

class SubscribeADmin(admin.ModelAdmin):
    list_display = (
        'user',
        'following',
    )
    list_filter = ('following', 'user')


admin.site.register(User)
admin.site.register(Subscribe)