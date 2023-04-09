from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS


User = get_user_model()


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_moderator
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_user

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
