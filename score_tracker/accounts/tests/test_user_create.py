from django.contrib.auth import get_user_model
import pytest

User = get_user_model()


@pytest.mark.django_db
class TestCreateGuestUserFunction:

    def test_if_created_guest_user_is_guest(self):

        # Arrange, Act
        user = User.objects.create_guest_user()

        # Assert
        assert user.is_guest is True
        # assert user.email is not None
        # assert user.password == ''


# TODO setup tests for email registration/email login logic

@pytest.mark.skip
class TestCreateUserFunction:

    """
    HAPPY PATHS
    """

    @pytest.mark.skip
    def test_user_can_login_using_email_field(self):
        pass

    """
    UNHAPPY PATHS
    """

    @pytest.mark.skip
    def test_user_cannot_login_using_username_field(self):
        pass

    @pytest.mark.skip
    def test_user_cannot_login_using_invalid_email_address(self):
        pass
