from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, signup, get_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)


app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/', include(router.urls))
    
]
