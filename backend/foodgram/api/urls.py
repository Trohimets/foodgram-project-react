from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import (RecipeViewSet, TagViewSet, IngredientViewSet,
                       FavoriteViewSet, CartViewSet, DownloadCartViewSet)
from users.views import UserViewSet, SubscribeViewSet


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register(
    'ingredients', IngredientViewSet,
    basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/download_shopping_cart/',
         CartViewSet.as_view({'get': 'download'}), name='download'),
    path('recipes/<recipes_id>/favorite/',
         FavoriteViewSet.as_view({'post': 'create',
                                  'delete': 'delete'}), name='favorite'),
    path('recipes/<recipes_id>/shopping_cart/',
         CartViewSet.as_view({'post': 'create',
                              'delete': 'delete'}), name='cart'),
    path('users/<users_id>/subscribe/',
         SubscribeViewSet.as_view({'post': 'create',
                                   'delete': 'delete'}), name='subscribe'),
    path('users/subscriptions/',
         SubscribeViewSet.as_view({'get': 'subscriptions'}), name='subscriptions'),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]