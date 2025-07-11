from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user and obj.author == request.user
                or request.method in SAFE_METHODS)


class NoDelete(BasePermission):
    def has_permission(self, request, view):
        return request.method != 'DELETE'
