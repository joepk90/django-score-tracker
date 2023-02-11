from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from model_bakery import baker
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


@pytest.fixture
def authenticate_as_guest(authenticate):
    def do_authenticate_as_guest():

        user = baker.make(User, is_guest=True)

        return authenticate(user=user)
    return do_authenticate_as_guest
