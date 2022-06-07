from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import (CartViewSet, FavoriteViewSet, IngredientViewSet,
                       RecipeViewSet, TagViewSet)
from users.views import SubscribeViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register(
    'ingredients', IngredientViewSet,
    basename='ingredients')

urlpatterns = [
    path('recipes/download_shopping_cart/',
         CartViewSet.as_view({'get': 'download'}), name='download'),
    path('users/subscriptions/',
         SubscribeViewSet.as_view({'get': 'list'}), name='subscriptions'),
    path('', include(router.urls)),
    path('recipes/<recipes_id>/favorite/',
         FavoriteViewSet.as_view({'post': 'create',
                                  'delete': 'delete'}), name='favorite'),
    path('recipes/<recipes_id>/shopping_cart/',
         CartViewSet.as_view({'post': 'create',
                              'delete': 'delete'}), name='cart'),
    path('users/<users_id>/subscribe/',
         SubscribeViewSet.as_view({'post': 'create',
                                   'delete': 'delete'}), name='subscribe'),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]