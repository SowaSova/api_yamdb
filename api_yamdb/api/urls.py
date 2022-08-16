from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet


router = DefaultRouter()
router.register('users', UsersViewSet, basename='post')


urlpatterns = [
    path('v1/', include(router.urls)),
]