from rest_framework import permissions, viewsets
from django.contrib.auth import get_user_model
from reviews.serializers import UserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny)
