import os

from rest_framework import permissions

from decouple import config

API_KEY = config('API_KEY')


class CustomPermissionOnlyGetProducts(permissions.BasePermission):

    view_methods = ("GET", "HEAD", "OPTIONS")

    def has_permission(self, request, view):

        if "API_KEY" in request.GET:
            api_key = request.GET["API_KEY"]
            if api_key == API_KEY:
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