from rest_framework import mixins, viewsets
from django.contrib.auth import get_user_model
from reviews.serializers import UserSerializer


User = get_user_model()


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class UserRegisterViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer