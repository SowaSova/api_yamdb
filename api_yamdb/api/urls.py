from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet, SignupViewSet, TokenViewSet


router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignupViewSet.as_view()),
    path('v1/auth/token/', TokenViewSet.as_view())
]
