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


EMAIL = "test@gmail.com"
PASSWORD = User.objects.make_random_password()
VALID_USER_CREDENTIALS = {
    "new_email": EMAIL,
    "password": PASSWORD
}


class TestUpdateGuestAccount:

    def if_anon_or_not_guest_return_401(update_guest_user):

        # Arrange, Act,
        response = update_guest_user(VALID_USER_CREDENTIALS)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def if_email_is_invalid_return_401(update_guest_user):

        # Arrange, Act
        response = update_guest_user({
            "new_email": "test",
            "password": PASSWORD
        })

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def if_email_is_not_provided_return_401(update_guest_user):

        # Arrange, Act
        response = update_guest_user({
            "password": PASSWORD
        })

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def if_password_is_invalid_return_401(update_guest_user):

        # Arrange, Act
        response = update_guest_user({
            "new_email": EMAIL,
            "password": "1234"
        })

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def if_password_is_not_provided_return_401(update_guest_user):

        # Arrange, Act
        response = update_guest_user({
            "new_email": EMAIL,
        })

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def if_email_and_password_is_not_provided_return_401(update_guest_user):

        # Arrange, Act
        response = update_guest_user({})

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    class TestAnonymousUser:

        """
        UNHAPPY PATHS
        """

        def test_if_anon_return_401(self, update_guest_user):

            # Arrange, Act, Assert
            TestUpdateGuestAccount.if_anon_or_not_guest_return_401(
                update_guest_user)

    @pytest.mark.django_db
    class TestGuestUser:

        """
        HAPPY PATHS
        """

        def test_set_user_credentials_return_200(self, authenticate_as_guest, update_guest_user):

            # Arrange,
            authenticate_as_guest()

           # Arrange, Act,
            response = update_guest_user(VALID_USER_CREDENTIALS)

            # Assert
            assert response.status_code == status.HTTP_200_OK
            assert response.data['new_email'] is not None
            assert response.data['password'] is not None
            # TODO this is bad - we shouldn't return users passwords...

        """
        UNHAPPY PATHS
        """

        def test_if_email_is_invalid_return_401(self, authenticate_as_guest, update_guest_user):

            # Arrange,
            authenticate_as_guest()

            # Act, Assert
            TestUpdateGuestAccount.if_email_is_invalid_return_401(
                update_guest_user)

        def test_if_email_is_not_provided_return_401(self, authenticate_as_guest, update_guest_user):

            # Arrange,
            authenticate_as_guest()

            # Act, Assert
            TestUpdateGuestAccount.if_email_is_not_provided_return_401(
                update_guest_user)

        def test_if_password_is_invalid_return_401(self, authenticate_as_guest, update_guest_user):

            # Arrange,
            authenticate_as_guest()

            # Act, Assert
            TestUpdateGuestAccount.if_password_is_invalid_return_401(
                update_guest_user)

        def test_if_password_is_not_provided_return_401(self, authenticate_as_guest, update_guest_user):

            # Arrange,
            authenticate_as_guest()

            # Act, Assert
            TestUpdateGuestAccount.if_password_is_not_provided_return_401(
                update_guest_user)

        def test_if_email_and_password_is_not_provided_return_401(self, authenticate_as_guest, update_guest_user):

            # Arrange,
            authenticate_as_guest()

            # Act, Assert
            TestUpdateGuestAccount.if_email_and_password_is_not_provided_return_401(
                update_guest_user)

        @pytest.mark.skip
        def test_if_user_updates_unrelated_account_return_401(self, authenticate, update_guest_user):

            # is this even possible to do/test?
            pass

        @pytest.mark.skip
        def test_if_user_requests_non_unique_email_address_return_401(self, authenticate, update_guest_user):

            pass

    @pytest.mark.django_db
    class TestDefaultUser:

        """
        UNHAPPY PATHS
        """

        def test_if_user_is_guest_return_401(self, authenticate, update_guest_user):

            # Arrange,
            user = baker.make(User)
            authenticate(user=user)

            # Act, Assert
            TestUpdateGuestAccount.if_anon_or_not_guest_return_401(
                update_guest_user)
