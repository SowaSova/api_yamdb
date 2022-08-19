from django.shortcuts import render, get_object_or_404, HttpResponse
from reviews.models import Review, Comment, Category, Genre, Title
from rest_framework import filters, mixins, pagination, viewsets
from .serializers import (CommentSerializer, ReviewSerializer, 
CategorySerializer, GenreSerializer, 
TitleSerializer)
from .permissions import StaffOrAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, StaffOrAuthorOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, StaffOrAuthorOrReadOnly]

    def create(self, request, *args, **kwargs):
        if self.serializer_class.is_valid():
            self.serializer_class.save(author=request.user)
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class ListCreateDestroyViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
        mixins.DestroyModelMixin, viewsets.GenericViewSet):

    pass


class CategoriesViewSet(ListCreateDestroyViewSet):
    """
    Получить список категорий, добавить или удалить
    категорию.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(ListCreateDestroyViewSet):
    """
    Получить список жанров, добавить или удалить
    жанр.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    """
    Получить список произведений и данные по одному
    произведению. Также Добавить произведение, изменить
    и удалить его.
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
