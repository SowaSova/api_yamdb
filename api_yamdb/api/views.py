from django.shortcuts import get_object_or_404
from reviews.models import Review, Comment, Category, Genre, Title
from rest_framework import filters, mixins, pagination, viewsets
from .serializers import (
    CommentSerializer, ReviewSerializer,
    CategorySerializer, GenreSerializer,
    TitleSerializer
)
from .permissions import StaffOrAuthorOrReadOnly, AdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ListCreateDestroyViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    """
    Комментарии к отзывам.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, StaffOrAuthorOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review, author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Только одно ревью к одному фильму.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, StaffOrAuthorOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if self.request.user.reviews.filter(title=title_id).exists():
            raise ValidationError('Только один отзыв на фильм')
        serializer.save(author=self.request.user, title=title)


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
