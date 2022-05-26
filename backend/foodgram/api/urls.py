from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import RecipeViewSet, TagViewSet, IngridientViewSet
from users.views import CreateUserView


router = DefaultRouter()
router.register('users', CreateUserView, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register(
    'ingridients', IngridientViewSet,
    basename='ingridients')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]