from rest_framework.viewsets import ModelViewSet
from . models import Score
from . serializers import ScoreSerializer
from rest_framework.throttling import ScopedRateThrottle


class ScoreViewSet(ModelViewSet):

    # allowed HTTP methods
    http_method_names = [
        'get',
        'post',
        'patch',
        # 'delete',
    ]

    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = []

    # throttling
    # https://medium.com/@nurettinabaci/drf-throttle-types-d885f0adebad
    # https://www.pedaldrivenprogramming.com/2017/05/throttling-django-rest-framwork-viewsets/
    # https://stackoverflow.com/questions/36039843/django-rest-post-and-get-different-throttle-scopes

    def get_throttles(self):
        if self.action == 'create':
            self.throttle_scope = 'scores.create'
            self.throttle_classes = [ScopedRateThrottle]

        return super().get_throttles()
