from djoser.serializers import UsernameSerializer, PasswordSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, \
    UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model
from django.core import exceptions as django_exceptions
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            # 'id',
            'email',
            'password',
            'first_name',
            'last_name',
        ]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            # 'id',
            'email',
            'first_name',
            'last_name',
        ]

# TODO there might be a more appropriate serializer to use in the jwt code


class UserAuthenticateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = [
            'email',
            'password',
        ]


# CUSTOM GUEST USER UPDATE SERIALIZER
# use to update an accounts credentials (username, password) after creation
# i think the validate code could be simplified by using nested serializer for the password field (PasswordSerializer)


# no fields are required as email is generated - might be checking if the email is unique
class GuestUserCreateSerializer(UserCreateSerializer):
    class Meta:
        fields = []


class GuestUpdateSerializer(UsernameSerializer):

    # TODO use nested validation
    # password = PasswordSerializer(required=True)

    class Meta(UsernameSerializer.Meta):

        # model = User
        fields = [
            # 'id',
            'email',
            'password',
        ]

    # TODO use nested validation instead -> PasswordSerializer
    # Djoser Serializer -> PasswordSerializer
    # https://github.com/sunscrapers/djoser/blob/abdf622f95dfa2c6278c4bd6d50dfe69559d90c0/djoser/serializers.py#L211
    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs
