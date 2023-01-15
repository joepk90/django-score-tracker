from djoser.serializers import UsernameSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, \
    UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
        ]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            'id',
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


class GuestUpdateSerializer(UsernameSerializer):
    class Meta(UsernameSerializer.Meta):
        pass
        # model = User
        fields = [
            # 'id',
            'email',
            'password',
        ]
