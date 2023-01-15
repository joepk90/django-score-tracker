# from rest_framework import permissions
from rest_framework.permissions import BasePermission
from score_tracker.exceptions import CustomAPIException
from rest_framework import status


def unauthorized_request():
    message = 'Permission denied: Unauthorized'
    raise CustomAPIException(
        detail=message,
        code=status.HTTP_401_UNAUTHORIZED
    )


class IsAuthenticatedAndIsObjectOwner(BasePermission):

    """
    Permission class to check that a user can access their own resources only
    """

    def has_object_permission(self, request, view,  obj):
        user = request.user
        if user.is_authenticated == False:
            unauthorized_request()

        return request.user == obj.user


class IsGuest(BasePermission):

    """
    Permission class to check that a user can access their own resources only
    """

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated == False:
            unauthorized_request()

        if user.is_guest != True:
            message = 'Cannot update credentials for non guest accounts'
            raise CustomAPIException(
                detail=message,
                code=status.HTTP_401_UNAUTHORIZED
            )

        return True

    def has_object_permission(self, request, view,  obj):
        return request.user == obj.user
