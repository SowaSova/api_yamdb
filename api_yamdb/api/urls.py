from .views import (
    ReviewViewSet, CommentViewSet, 
    CategoriesViewSet, GenresViewSet, 
    TitlesViewSet
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register(r'categories', CategoriesViewSet, basename='category')
router.register(r'genres', GenresViewSet, basename='genre')
router.register(r'titles', TitlesViewSet, basename='title')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='review')
router.register(r'/titles/?P<title_id>\d+)/reviews/?P<review_id>\d+)/comments/',
                CommentViewSet, basename='comment')



urlpatterns = [
    path('v1/', include(router.urls)),
]

