from rest_framework import serializers
from . models import Score


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
        score = Score.objects.create(
            user=user,
            **validated_data
        )
        return score


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = [
            "id",
            'number',
            'date',
            # 'user'
        ]

# TODO
# phase 2
# allow option to attach user to a score record (by ID or by using the request auth token?)
# - make secure! should other users be allowed to view anyones score?
# list all scores by a certain user /scores/me OR scores/user_id ?
