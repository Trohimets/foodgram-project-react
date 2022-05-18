from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import viewsets

from api.serializers import (RecipeSerializer, TagSerializer,
                          IngridientSerializer, UserSerializer)
from recipes.models import User, Tag, Recipe, Ingridient


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class IngridientViewSet(viewsets.ModelViewSet):
    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer

# Ещё ендпоинты:
# Главная страница - рецепты 6 штук, пагинация
# Страница пользователя - имя пользователя, все рецепты, возможность подписаться на него
# Подписка на авторов - авториз
# Избранное - авториз
# Список покупок - авториз