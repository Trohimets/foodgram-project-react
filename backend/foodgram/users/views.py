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
from foodgram.settings import DEFAULT_FROM_EMAIL


FIELD_ERROR = 'Неуникальное поле. Пользователь с таким {} уже существует'

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, created = User.objects.get_or_create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],
        )
    except IntegrityError as error:
        raise ValidationError(FIELD_ERROR.format(f'{error}'.partition('.')[2]))
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        SUBJECT,
        MESSAGE.format(confirmation_code),
        DEFAULT_FROM_EMAIL,
        [user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password'],
    )
    token = AccessToken.for_user(user)
    data = {
        'token': str(token),
    }
    return Response(f'"auth_token": "{data}"')


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
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = [IsAdmin | ReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)