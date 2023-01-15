from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import re_path
from . views import CustomDjsoserUserViewSet

router = DefaultRouter()
router.register("users", CustomDjsoserUserViewSet)


# TODO: enable djoser auth endpoints if authenticated as super user


urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

urlpatterns += router.urls
