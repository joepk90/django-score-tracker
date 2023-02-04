from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from . models import Score
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class ScoreGuestUserCreateResponseSerializer(serializers.ModelSerializer):

    tokens = serializers.SerializerMethodField()

    class Meta:
        model = Score
        fields = [
            # "id",
            "uuid",
            'number',
            'date',
            "tokens",
        ]

    def get_tokens(self, obj):
        refresh_token = RefreshToken.for_user(obj.user)
        access_token = AccessToken.for_user(obj.user)
        return {
            "refresh": str(refresh_token),
            "access": str(access_token)
        }


class ScoreGuestUserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = [
            # "id",
            # "uuid",
            # 'date',
            'number',
            # 'user_id',
        ]

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_guest_user()
            validated_data["user_id"] = user.id
            return super().create(validated_data)

    # TODO seperation of concerns - perhaps make seperate request to authenticate as guest user...?
    def to_representation(self, instance):
        # return super().to_representation(instance)
        serializer = ScoreGuestUserCreateResponseSerializer(instance)
        return serializer.data


class ScoreUserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = [
            # "id",
            'uuid',
            'number',
            'date',
            # 'user_id',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data["user_id"] = user.id
        return super().create(validated_data)


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = [
            # "id",
            "uuid",
            'number',
            'date',
            # 'time',
            # 'time_updated',
            # 'user_id'
        ]

# TODO
# phase 2
# allow option to attach user to a score record (by ID or by using the request auth token?)
# - make secure! should other users be allowed to view anyones score?
# list all scores by a certain user /scores/me OR scores/user_id ?
