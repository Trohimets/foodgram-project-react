from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import RecipeViewSet, TagViewSet, IngredientViewSet
from users.views import UserViewSet
# CreateUserView, UserDetail


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register(
    'ingredients', IngredientViewSet,
    basename='ingredients')

urlpatterns = [
#    path('api/users/<int:id>/', user_detail),
#    path('api/users/<int:id>/', UserDetail.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]