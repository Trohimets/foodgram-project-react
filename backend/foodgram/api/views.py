from rest_framework import viewsets

from api.serializers import (RecipeSerializer, TagSerializer,
                             IngridientSerializer)
from recipes.models import Tag, Recipe, Ingridient


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