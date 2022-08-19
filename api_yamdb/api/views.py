from django.shortcuts import get_object_or_404
from reviews.models import Review, Comment, Category, Genre, Title
from rest_framework import filters, mixins, pagination, viewsets
from .serializers import (
    CommentSerializer, ReviewSerializer,
    CategorySerializer, GenreSerializer,
    TitleSerializer, SignupSerializer, TokenSerializer
)
from .permissions import StaffOrAuthorOrReadOnly, AdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


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


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username']
        )

        confirmation_code = default_token_generator.make_token(user)
        confirmation_code_hashed = make_password(confirmation_code, salt='well')

        user.confirmation_code = confirmation_code_hashed
        user.save()

        send_mail(
            'Код подтверждения',
            f'{user.username}, ваш код: {confirmation_code} /api/v1/auth/token/',
            'from_russia@with_love.ru',
            [f'{user.email}'])
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(username=serializer.initial_data['username'])
        c_code = serializer.initial_data['confirmation_code']
        if check_password(c_code, user.confirmation_code):
            refresh = RefreshToken.for_user(user)
            return Response({'access': str(refresh.access_token)})

    return Response(serializer.errors)
