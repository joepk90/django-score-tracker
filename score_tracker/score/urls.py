from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import ScoreViewSet

router = DefaultRouter()
router.register("", ScoreViewSet)

urlpatterns = router.urls
