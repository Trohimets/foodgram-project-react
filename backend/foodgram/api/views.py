from requests import request
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework import filters
from http import HTTPStatus
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from api.serializers import (RecipeGetSerializer, TagSerializer,
                             RecipePostSerializer, BaseIngredientSerializer,
                             FavoriteSerializer, CartSerializer)
from recipes.models import Tag, Recipe, Ingredient, Favorite, Cart


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    filterset_fields = ('author', 'tags')
    ordering_fields = ('name', 'id')
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = RecipeGetSerializer(instance=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = RecipeGetSerializer(instance=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = BaseIngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    model = Favorite

    def create(self, request, *args, **kwargs):
        recipe_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            return Response({
                'errors': 'Рецепт уже добавлен в Избранное'
            }, status=status.HTTP_400_BAD_REQUEST)
        self.model.objects.create(
            user=request.user, recipe=recipe)
        serializer = FavoriteSerializer()
        return Response(serializer.to_representation(instance=recipe),
                    status=status.HTTP_201_CREATED
                )

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipes_id']
        user_id = request.user.id
        object = get_object_or_404(
            self.model, user__id=user_id, recipe__id=recipe_id)
        object.delete()
        return Response(HTTPStatus.NO_CONTENT)


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    model = Cart

    def create(self, request, *args, **kwargs):
        recipe_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if Cart.objects.filter(user=request.user, recipe=recipe).exists():
            return Response({
                'errors': 'Рецепт уже добавлен в список покупок'
            }, status=status.HTTP_400_BAD_REQUEST)
        self.model.objects.create(
            user=request.user, recipe=recipe)
        serializer = CartSerializer()
        return Response(serializer.to_representation(instance=recipe),
                    status=status.HTTP_201_CREATED
                )

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipes_id']
        user_id = request.user.id
        object = get_object_or_404(
            self.model, user__id=user_id, recipe__id=recipe_id)
        object.delete()
        return Response(HTTPStatus.NO_CONTENT)

    def download(self, request):
        shopping_cart = Cart.objects.filter(user=request.user).all()
        shopping_list = {}
        for item in shopping_cart:
            for recipe_ingredient in item.recipe.recipe_ingredients.all():
                name = recipe_ingredient.ingredient.name
                measuring_unit = recipe_ingredient.ingredient.measurement_unit
                amount = recipe_ingredient.amount
                if name not in shopping_list:
                    shopping_list[name] = {
                        'name': name,
                        'measurement_unit': measuring_unit,
                        'amount': amount
                    }
                else:
                    shopping_list[name]['amount'] += amount
        content = (
            [f'{item["name"]} ({item["measurement_unit"]}) '
            f'- {item["amount"]}\n'
            for item in shopping_list.values()]
        )
        filename = 'shopping_list.txt'
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename={0}'.format(filename)
        )
        return response

class DownloadCartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cart.objects.all()
    model = Cart
    
    def download(self, request):
        shopping_cart = Cart.objects.filter(user=request.user).all()
        shopping_list = {}
        for item in shopping_cart:
            for recipe_ingredient in item.recipe.recipe_ingredients.all():
                name = recipe_ingredient.ingredient.name
                measuring_unit = recipe_ingredient.ingredient.measurement_unit
                amount = recipe_ingredient.amount
                if name not in shopping_list:
                    shopping_list[name] = {
                        'name': name,
                        'measurement_unit': measuring_unit,
                        'amount': amount
                    }
                else:
                    shopping_list[name]['amount'] += amount
        content = (
            [f'{item["name"]} ({item["measurement_unit"]}) '
            f'- {item["amount"]}\n'
            for item in shopping_list.values()]
        )
        filename = 'shopping_list.txt'
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename={0}'.format(filename)
        )
        return response
