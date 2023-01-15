from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import CustomDjsoserUserViewSet
from . views import GuestUserUpdateViewSet

router = DefaultRouter()
router.register("guest", GuestUserUpdateViewSet)
router.register("users", CustomDjsoserUserViewSet)


urlpatterns = [
    path('', include('djoser.urls.jwt')),
]

urlpatterns += router.urls
