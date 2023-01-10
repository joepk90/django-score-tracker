from rest_framework.viewsets import GenericViewSet
from . models import Score
from . serializers import ScoreSerializer, ScoreUserCreateSerializer
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, \
    RetrieveModelMixin, \
    UpdateModelMixin \



class ScoreViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):

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

    def get_serializer_class(self):

        user = self.request.user
        if user.is_authenticated and self.action == 'create':
            return ScoreUserCreateSerializer

        return ScoreSerializer

    # custom endpoints

    @action(detail=False, methods=["get"])
    def today(self, request):
        # scores = self.get_queryset().filter(date="Today")
        scores = self.get_queryset()
        serializer = self.get_serializer(scores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def me(self, request):
        # scores = self.get_queryset().filter(date="Today")
        scores = self.get_queryset()
        serializer = self.get_serializer(scores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
