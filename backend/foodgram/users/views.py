from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import User
from rest_framework import permissions, status
from rest_framework.decorators import action
from api.paginations import LimitPageNumberPagination
from rest_framework.response import Response
from users.models import Subscribe
from users.serializers import SubShowSerializer


class CustomUserViewSet(UserViewSet):

    queryset = User.objects.all()
    pagination_class = LimitPageNumberPagination

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        url_path='subscribe',
        permission_classes=[permissions.IsAuthenticatedOrReadOnly],
    )
    def subscribe(self, request, id=None):
        user = get_object_or_404(User, id=id)
        follow = Subscribe.objects.filter(
            user=request.user,
            following=user
        )
        if request.method == 'POST':
            if user == request.user:
                error = {
                    'errors': 'Вы пытаетесь подписаться на себя.'
                }
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            obj, created = Subscribe.objects.get_or_create(
                user=request.user,
                following=user
            )
            if not created:
                error = {
                    'errors': 'Вы уже подписаны на этого пользователя.'
                }
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            serializer = SubShowSerializer(obj, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not follow.exists():
            error = {
                'errors': 'Вы не были подписаны на этого пользователя.'
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('GET',),
        permission_classes=[permissions.IsAuthenticatedOrReadOnly],
    )
    def subscriptions(self, request):
        pages = self.paginate_queryset(
            Subscribe.objects.filter(user=request.user)
        )


        serializer = SubShowSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
