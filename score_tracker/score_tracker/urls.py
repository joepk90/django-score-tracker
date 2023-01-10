"""score_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.debug import default_urlconf

# enable developement page
# https://stackoverflow.com/questions/55110493/how-to-retain-the-development-page
# https://stackoverflow.com/questions/14951468/who-generates-the-default-page-of-django-welcome-page

urlpatterns = [
    path('', default_urlconf),
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),  # djoser urls
    path('scores/', include('score.urls')),
]

# default djoser urls (add to interact with live db)
# path('auth/', include('djoser.urls')),
# path('auth/', include('djoser.urls.jwt')),
