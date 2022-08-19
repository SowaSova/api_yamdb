from django.shortcuts import render, get_object_or_404, HttpResponse
from reviews.models import Review, Comment
from rest_framework import filters, mixins, pagination, viewsets
from .serializers import CommentSerializer, ReviewSerializer
from .permissions import StaffOrAuthorOrReadOnly

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
