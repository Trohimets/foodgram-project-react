
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import generics
from rest_framework import viewsets
from users.serializers import (RegistrationSerializer, UserDetailSerializer)
from api.permissions import IsAdmin, ReadOnly
from recipes.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from djoser.views import UserViewSet
from rest_framework import status


#class CreateUserView(UserViewSet):
#    serializer_class = RegistrationSerializer
#    permission_classes = (AllowAny,)
#    lookup_field = 'username'

#    def get_queryset(self):
#        return User.objects.all()
#
#    def get_permissions(self):
#        if self.action == 'create':
#            permission_classes = [AllowAny]
#        elif self.action == 'actioned':
#            permission_classes = [IsAuthenticated]
#        else:
#            permission_classes = [AllowAny]
#        return [permission() for permission in permission_classes]



#@api_view(['GET'])
#@permission_classes([AllowAny])
#def user_detail(request, id):
#    user = get_object_or_404(User, id=id)
#    serializer = RegistrationSerializer(user)
#    return Response(serializer.data)

#class UserDetail(generics.RetrieveAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserDetailSerializer


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