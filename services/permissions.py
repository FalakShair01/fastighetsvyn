# permissions.py
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read access to all users
        if request.user.is_authenticated and request.method in permissions.SAFE_METHODS:
            return True

        # Allow write access only to admins
        return request.user.is_authenticated and request.user.role == "ADMIN"
