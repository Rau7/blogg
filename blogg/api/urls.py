from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import PostViewSet, login_view, register_view, UserViewSet, CurrentUserAPIView, DashboardView
from rest_framework import routers


router = routers.DefaultRouter();


router.register('posts', PostViewSet)

router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),
    path('current_user/', CurrentUserAPIView.as_view() , name='current_user'),
    path('dashboard/', DashboardView.as_view({'get': 'list'}) , name='dashboard'),
]
