from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserRegisterViewSet


urlpatterns = [
    path('v1/auth/signup/', UserRegisterViewSet.as_view)
]
