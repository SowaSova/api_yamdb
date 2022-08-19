from rest_framework import permissions, viewsets, views
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from api.serializers import UserSerializer
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from api.permissions import AuthorOrAdmin


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AuthorOrAdmin,)
    lookup_field = 'username'


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
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
        print(confirmation_code, user.confirmation_code)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['POST'])
def get_token(request):
    serializer = UserSerializer(data=request.data)
    # if serializer.is_valid():
    user = User.objects.get(username=serializer.initial_data['username'])
    c_code = serializer.initial_data['confirmation_code']
    if check_password(c_code, user.confirmation_code):
        refresh = RefreshToken.for_user(user)
        return Response({'access': str(refresh.access_token)})

    return Response({'well': 'soso'})