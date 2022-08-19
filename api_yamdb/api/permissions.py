from rest_framework.permissions import BasePermission


class AuthorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 3 or view.action in ['retrieve']

    def has_object_permission(self, request, view, obj):
        return request.user.role == 3 or obj == request.user
