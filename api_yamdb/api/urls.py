from .views import (
    ReviewViewSet, CommentViewSet,)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register(r'title/')
