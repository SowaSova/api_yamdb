from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'categories', CategoriesViewSet, basename='category')
router.register(r'genres', GenresViewSet, basename='genre')
router.register(r'titles', TitlesViewSet, basename='title')


urlpatterns = [
    path('v1/', include(router.urls)),
]
