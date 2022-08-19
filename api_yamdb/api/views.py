from rest_framework import viewsets, mixins, filters
from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import AdminOrReadOnly


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
