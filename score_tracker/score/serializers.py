from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from . models import Score
from django.contrib.auth import get_user_model
import uuid


class ScoreGuestUserCreateResponseSerializer(serializers.ModelSerializer):

    tokens = serializers.SerializerMethodField()

    class Meta:
        model = Score
        fields = [
            "id",
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
            "id",
            'number',
            'date',
        ]

    def create(self, validated_data):
        # TODO make auto-generated email logic default functionality of user model when is_guest=True
        email = f"{uuid.uuid4().hex}"
        User = get_user_model()
        user = User.objects.create(
            is_guest=True,
            email=email
        )

        score = Score.objects.create(
            user=user,
            **validated_data
        )
        score.access_token = "hello"
        return score

    def to_representation(self, instance):
        print("instance", instance)
        serializer = ScoreGuestUserCreateResponseSerializer(instance)
        return serializer.data


class ScoreUserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = [
            "id",
            'number',
            'date',
            # 'user',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data["user"] = user
        return super().create(validated_data)


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = [
            "id",
            'number',
            'date',
            # 'time',
            # 'time_updated',
            # 'user'
        ]

# TODO
# phase 2
# allow option to attach user to a score record (by ID or by using the request auth token?)
# - make secure! should other users be allowed to view anyones score?
# list all scores by a certain user /scores/me OR scores/user_id ?
