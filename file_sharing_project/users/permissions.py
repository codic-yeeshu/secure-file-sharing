# users/permissions.py
from rest_framework import permissions

class IsOpsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and 
                request.user.user_type == 'ops')

class IsClientUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and 
                request.user.user_type == 'client')