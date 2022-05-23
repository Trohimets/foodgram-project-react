from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsAdmin(BasePermission):
    message = 'Пользователь не является администратором!'

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.is_admin
        )


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
