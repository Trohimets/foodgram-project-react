from django.contrib import admin
from users.models import User


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