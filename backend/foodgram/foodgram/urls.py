from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views


urlpatterns = [
    path('api/', include('api.urls')),
    path('api/auth/token/login/', views.obtain_auth_token),
    path('admin/', admin.site.urls)
]
