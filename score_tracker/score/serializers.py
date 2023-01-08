from rest_framework import serializers
from . models import Score


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = [
            "id",
            'number',
            'date'
            # 'user', # TODO setup logic to attach user_id to score record
        ]

# TODO
# phase 1 (mvp)
# list all scores from all users, without showing the user id
# prevent users submitting another score on the same day
#  - no real way to prevent this, this should probobly be handled client side...


# phase 2
# list all scores by a certain user /scores/me OR scores/user_id ?
