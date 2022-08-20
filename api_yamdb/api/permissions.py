from rest_framework import permissions


class StaffOrAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method == 'POST' and request.user.is_authenticated
            or request.method in ['PATCH', 'DELETE'] and (
                request.user.role in ['moderator', 'admin']
                or request.user == obj.author)
        )


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.role == 'admin')
        )


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.role == 'admin'
            or user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and user.role == 'admin'
            or user.is_superuser
        )


class AuthorOrAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            self.method in permissions.SAFE_METHODS
            or self.method == 'POST' and request.user.is_authenticated
            or self.method in ['PATCH', 'DELETE'] and request.user.role in ['admin', 'moderator']
        )
