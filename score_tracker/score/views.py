from rest_framework.viewsets import ModelViewSet
from . models import Score
from . serializers import ScoreSerializer


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
