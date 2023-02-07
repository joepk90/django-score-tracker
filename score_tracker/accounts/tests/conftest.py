from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(user=None):

        if user == None:
            user = user = User()

        return api_client.force_authenticate(user=user)
    return do_authenticate
