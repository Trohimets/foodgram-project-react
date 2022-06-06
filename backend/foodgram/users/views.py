
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from api.serializers import (
    RegistrationSerializer,
    UserDetailSerializer,
    SubscribeSrializer)
from users.models import User, Subscribe
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserDetailSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserDetailSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscribeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    #queryset = Subscribe.objects.filter(user=request.user)

    def create(self, request, *args, **kwargs):
        followed = get_object_or_404(User, id=id)
        follower = request.user
        if Subscribe.objects.filter(user=follower, following=followed).exists():
            return Response({
                'errors': 'Вы и так уже подписаны'
            }, status=status.HTTP_400_BAD_REQUEST)
        subscribe = Subscribe.objects.create(
            user=follower, following=followed)
        serializer = SubscribeSrializer()
        return Response(serializer.to_representation(instance=subscribe.author),
                    status=status.HTTP_201_CREATED
                )

    def delete(self, request, *args, **kwargs):
        followed = get_object_or_404(User, id=id)
        follower = request.user
        object = get_object_or_404(
            Subscribe, user=follower, following=followed)
        object.delete()
        return Response(status.HTTP_204_NO_CONTENT)