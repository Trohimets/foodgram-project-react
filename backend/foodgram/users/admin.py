from django.contrib import admin
from users.models import User


class UserADmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email'
    )
    list_filter = ('first_name', 'email')


admin.site.register(User)