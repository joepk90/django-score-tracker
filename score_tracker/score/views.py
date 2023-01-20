from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from . models import Score
from . serializers import ScoreSerializer, ScoreUserCreateSerializer, ScoreGuestUserCreateSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, \
    RetrieveModelMixin, \
    UpdateModelMixin
from accounts.permissions import IsAuthenticatedAndIsObjectOwner
from rest_framework.exceptions import APIException
from datetime import datetime
from score_tracker.exceptions import CustomAPIException
from score_tracker.throttles import DailyRateThrottle
from django.conf import settings


class ScoreViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):

    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticatedAndIsObjectOwner]

    # throttling
    # https://medium.com/@nurettinabaci/drf-throttle-types-d885f0adebad
    # https://www.pedaldrivenprogramming.com/2017/05/throttling-django-rest-framwork-viewsets/
    # https://stackoverflow.com/questions/36039843/django-rest-post-and-get-different-throttle-scopes

    def get_throttles(self):

        if settings.DEBUG == True:
            return super().get_throttles()

        if self.action == 'create':
            # self.throttle_scope = 'scores.create'
            self.throttle_classes = [DailyRateThrottle]
        return super().get_throttles()

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated == True and (self.action == 'create' or self.action == 'list'):
            return ScoreUserCreateSerializer
        elif user.is_authenticated == False and (self.action == 'create' or self.action == 'list'):
            return ScoreGuestUserCreateSerializer

        return ScoreSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super(self.__class__, self).get_permissions()

    def perform_create(self, serializer):

        if settings.DEBUG == True:
            return super().perform_create(serializer)

        user = self.request.user
        score = Score.objects.filter(user_id=user.id, date=datetime.today())

        if score:
            message = 'User can only create one score per day'
            raise CustomAPIException(
                detail=message,
                code=status.HTTP_401_UNAUTHORIZED
            )

        return super().perform_create(serializer)

    def perform_update(self, serializer):
        id = self.kwargs.get('pk', None)
        post = Score.objects.get(id=id)
        today = datetime.utcnow().date()

        if post.date < today:
            message = 'Scores created on previous days cannot be updated.'
            raise CustomAPIException(
                detail=message,
                code=status.HTTP_401_UNAUTHORIZED
            )

        return super().perform_update(serializer)

    # custom endpoints

    # action not fully function
    # - why does @action detail need to = False?
    # - should try use default actions: retreive, update
    #  - currenly cannot update
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated, IsAuthenticatedAndIsObjectOwner])
    def today(self, request):
        user = self.request.user
        date_today = datetime.utcnow().strftime('%Y-%m-%d')
        score = self.get_queryset().get(user_id=user.id, date=date_today)
        serializer = self.get_serializer(score, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def me(self, request):
        # scores = self.get_queryset().filter(date="Today")
        scores = self.get_queryset()
        serializer = self.get_serializer(scores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
