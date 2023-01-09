from rest_framework import serializers
from . models import Score


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = [
            "id",
            'number',
            'date'
            # 'user', # TODO request params or by user id?
        ]

# TODO
# phase 2
# allow option to attach user to a score record (by ID or by using the request auth token?)
# list all scores by a certain user /scores/me OR scores/user_id ?
