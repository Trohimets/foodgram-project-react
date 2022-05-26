
from rest_framework.permissions import AllowAny

from users.serializers import (RegistrationSerializer)
from api.permissions import IsAdmin, ReadOnly
from recipes.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from djoser.views import UserViewSet

class CreateUserView(UserViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.all()