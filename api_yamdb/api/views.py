from django.shortcuts import get_object_or_404
from reviews.models import Review, Category, Genre, Title
from rest_framework import filters, mixins, viewsets, status
from .serializers import (
    CommentSerializer, ReviewSerializer,
    CategorySerializer, GenreSerializer,
    TitleSerializer, SignupSerializer, TokenSerializer, UserSerializer,
    TitleDisplaySerializer, AdminSerializer
)
from .permissions import StaffOrAuthorOrReadOnly, AdminOrReadOnly, IsAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import django_filters
from django_filters import rest_framework


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
    permission_classes = (StaffOrAuthorOrReadOnly,)

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
    permission_classes = [StaffOrAuthorOrReadOnly]

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
    lookup_field = 'slug'
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
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleFilter(django_filters.FilterSet):
    category = rest_framework.CharFilter(field_name='category__slug')
    genre = rest_framework.CharFilter(field_name='genre__slug')
    name = rest_framework.CharFilter(
        field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = {
            'year': ['exact']
        }


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
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleDisplaySerializer
        return super().get_serializer_class()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Принимает почту и юзернейм, в ответ отправляет
    код подтверждения.
    """
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = User.objects.create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username']
        )

        confirmation_code = default_token_generator.make_token(user)
        confirmation_code_hashed = make_password(
            confirmation_code, salt='well')

        user.confirmation_code = confirmation_code_hashed
        user.save()

        send_mail(
            'Код подтверждения',
            f'{user.username}, код: {confirmation_code} /api/v1/auth/token/',
            'from_russia@with_love.ru',
            [f'{user.email}'])
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """
    Принимает код подтверждения, сравнивает его с хешем.
    В ответ отправляет токен.
    """
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        c_code = serializer.initial_data['confirmation_code']
        if check_password(c_code, user.confirmation_code):
            refresh = RefreshToken.for_user(user)
            return Response({'access': str(refresh.access_token)})
        raise ValidationError()

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Админ может получить список пользователей, добаввить
    одного. Получить, изменить его данные. Удалить его.
    Сам пользователь может получить и изменить свои данные.
    """
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False, methods=['get', 'patch'],
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def about_me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)
