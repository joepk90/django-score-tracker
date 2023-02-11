from django.contrib.auth import get_user_model
from rest_framework import status
from model_bakery import baker
import pytest

User = get_user_model()


@pytest.fixture
def update_guest_user(api_client):
    def do_update_guest_user(user_credentials):
        return api_client.put(f'/auth/guest/', user_credentials)
    return do_update_guest_user


class TestUpdateGuestAccount:

    class TestAnonymousUser:

        """
        UNHAPPY PATHS
        """

        def test_should_return_401(self, update_guest_user):

            #  arrange
            user_credentials = {
                "new_email": "test@gmail.com",
                "password": "hasnsdeurnahfaa78awen"
            }

            # act
            response = update_guest_user(user_credentials)

            # assert
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.skip
    class TestGuestUser:

        def test_set_user_credentials():
            pass

            user = baker.make(User)

    @pytest.mark.skip
    class TestDefaultUser:
        pass
