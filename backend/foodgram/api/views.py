from http import HTTPStatus
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response

from api.filters import AuthorAndTagFilter
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from api.serializers import (BaseIngredientSerializer, CartSerializer,
                             FavoriteSerializer, RecipeGetSerializer,
                             RecipePostSerializer, TagSerializer)
from api.paginations import LimitPageNumberPagination
from foodgram.settings import FILENAME
from recipes.models import Cart, Favorite, Ingredient
from recipes.models import Recipe, Tag, IngredientMount


CONTENT_TYPE = 'text/plain'


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AuthorAndTagFilter
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = LimitPageNumberPagination

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
        #headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
                        #headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = RecipeGetSerializer(instance=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_200_OK,
                        headers=headers)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = BaseIngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    model = Favorite

    def create(self, request, *args, **kwargs):
        recipe_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipe_id)
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
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CartSerializer
    pagination_class = LimitPageNumberPagination
    queryset = Cart.objects.all()
    model = Cart

    def create(self, request, *args, **kwargs):
        recipe_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipe_id)
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
        shopping_list = IngredientMount.objects.filter(
            recipe__shopping_cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').order_by(
                'ingredient__name').annotate(ingredient_total=Sum('amount'))

        content = (
         [f'{item["ingredient__name"]} ({item["ingredient__measurement_unit"]})'
          f'- {item["ingredient_total"]}\n'
          for item in shopping_list]
                   )
        response = HttpResponse(content, content_type=CONTENT_TYPE)
        response['Content-Disposition'] = (
            f'attachment; filename={FILENAME}'
        )
        return response