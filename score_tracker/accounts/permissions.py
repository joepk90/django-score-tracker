# from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthenticatedAndIsObjectOwner(BasePermission):

    """
    Permission class to check that a user can access their own resources only
    """

    def has_object_permission(self, request, view,  obj):
        return request.user == obj.user
