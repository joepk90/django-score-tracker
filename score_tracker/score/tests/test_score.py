from django.contrib.auth import get_user_model
from rest_framework import status
from model_bakery import baker
import pytest
from score.models import Score


# baker will dynamically create objects (including model relationships)

# make db connection
# @pytest.mark.django_db

# skip test
# @pytest.mark.skip

# test format
# Arrange, Act, Assert

User = get_user_model()


@pytest.fixture
def delete_score(api_client):
    def do_delete_score(uuid):
        return api_client.delete(f'/score/{uuid}/')
    return do_delete_score


@pytest.mark.django_db
class TestDeleteScore:

    class TestAnonymousUser:

        """
        UNHAPPY PATHS
        """

        def test_if_user_requests_to_delete_score_return_401(self, delete_score):

            # Arrange
            score = baker.make(Score)

            # Act
            response = delete_score(score.uuid)

            # Assert
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    class TestGuestAndDefaultUser:

        """
        UNHAPPY PATHS
        """

        def test_if_user_to_delete_score_they_made_return_401(self, authenticate, delete_score):

            # Arrange
            user = baker.make(User)
            score = baker.make(Score, user_id=user.id)
            authenticate(user=user)

            # Act
            response = delete_score(score.uuid)

            # Assert
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestScoreIntToDecimalConversion():

    """
    UNHAPPY PATHS
    """

    def test_if_invalid_int_numbers_are_rejected(self, authenticate, update_score):

        # Arrange
        user = baker.make(User)
        score = baker.make(Score, user_id=user.id)
        authenticate(user=user)
        numbers = [
            0.001,
            # -0, # this passes!
            10.001,
            11
        ]

        for number in numbers:

            # Act,
            response = update_score(score.uuid, {'number': number})

            # Assert
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    """
    HAPPY PATHS
    """

    def test_if_int_numbers_are_correctly_saved_as_decimals(self, authenticate, update_score):

        # Arrange
        user = baker.make(User)
        score = baker.make(Score, user_id=user.id)
        authenticate(user=user)
        numbers = {
            0: '0.00',
            0.5: '0.50',
            0.05: '0.05',
            1: '1.00',
            10: '10.00'
        }
        # numbers = [0.001, -0, 10.001, 11]

        for input_number, output_number in numbers.items():

            # Act,
            response = update_score(score.uuid, {'number': input_number})

            # Assert
            assert response.data['number'] == output_number
