import os

from rest_framework import permissions


class CustomPermissionOnlyGetProducts(permissions.BasePermission):

    view_methods = ("GET", "HEAD", "OPTIONS")

    def has_permission(self, request, view):

        if "HTTP_API_KEY" in request.META:
            API_KEY = request.META["HTTP_API_KEY"]
            if API_KEY == os.getenv("API_KEY"):
                return True
            return False
        
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return False

        if request.method in permissions.SAFE_METHODS:
            return False

        if request.user.is_staff and request.method not in self.view_methods:
            return False

        return False