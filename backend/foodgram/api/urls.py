from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CartViewSet, FavoriteViewSet, IngredientViewSet,
                       RecipeViewSet, TagViewSet)

router = DefaultRouter()

router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register(
    'ingredients', IngredientViewSet,
    basename='ingredients')

urlpatterns = [
    path('', include('users.urls')),
    path('recipes/download_shopping_cart/',
         CartViewSet.as_view({'get': 'download'}), name='download'),
    path('', include(router.urls)),
    path('recipes/<recipes_id>/favorite/',
         FavoriteViewSet.as_view({'post': 'create',
                                  'delete': 'delete'}), name='favorite'),
    path('recipes/<recipes_id>/shopping_cart/',
         CartViewSet.as_view({'post': 'create',
                              'delete': 'delete'}), name='cart'),
]
