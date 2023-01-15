from django.core import exceptions as django_exceptions
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from djoser.views import UserViewSet
from . permissions import IsGuest
from . serializers import GuestUpdateSerializer

User = get_user_model()


class CustomDjsoserUserViewSet(UserViewSet):
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options',
    ]


class GuestUserUpdateViewSet(UserViewSet):

    queryset = User.objects.all()
    serializer_class = GuestUpdateSerializer
    # permission_classes = [AllowAny] # for debugging
    permission_classes = [IsAuthenticated, IsGuest]

    http_method_names = [
        'put',
    ]

    # DRF UpdateModelMixin -> update method:
    # https://github.com/encode/django-rest-framework/blob/0618fa88e1a8c2cf8a2aab29ef6de66b49e5f7ed/rest_framework/mixins.py#L65
    @action(detail=False, methods=["put"])
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.request.user
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # move password validation to serializer
        try:
            validate_password(serializer.data["password"], instance)
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": list(e.messages)})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        self.queryset = User.objects.all().filter(id=user.id)
        return super().get_queryset()

    def perform_update(self, serializer, *args, **kwargs):

        # calls djoser SEND_ACTIVATION logic
        super().perform_update(serializer, *args, **kwargs)

        new_username = serializer.data["new_" + User.USERNAME_FIELD]
        new_password = serializer.data["password"]

        user = serializer.instance
        setattr(user, User.USERNAME_FIELD, new_username)
        setattr(user, "password", make_password(new_password))
        setattr(user, "is_guest", False)
        user.save()
