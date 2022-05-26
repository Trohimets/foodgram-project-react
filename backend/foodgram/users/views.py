from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status, viewsets, filters, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.serializers import (UserSerializer,
                              TokenSerializer)
from api.permissions import IsAdmin, ReadOnly
from recipes.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'username'

    @action(
        methods=['get', 'post', 'patch'],
        detail=False,
        permission_classes=(AllowAny,),
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
                request.user,
                data=request.data
            )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)