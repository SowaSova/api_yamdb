from django.shortcuts import render
from rest_framework import viewsets
from reviews.models import User
from .serializers import UserSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
