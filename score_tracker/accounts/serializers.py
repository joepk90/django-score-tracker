from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, \
    UserSerializer as BaseUserSerializer


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
