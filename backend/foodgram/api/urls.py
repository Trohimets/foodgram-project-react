from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import RecipeViewSet, TagViewSet, IngridientViewSet


router_v1 = DefaultRouter()
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register(
    'ingridients', IngridientViewSet,
    basename='ingridients')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]