from django.contrib.auth import get_user_model
from rest_framework import status
from model_bakery import baker
import pytest

User = get_user_model()


@pytest.fixture
def update_score(api_client):
    def do_update_score():
        return api_client.put(f'/auth/guest/')
    return do_update_score


@pytest.mark.skip
class GuestAccount:

    def test_set_user_credentials():
        pass
