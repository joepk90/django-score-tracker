from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from model_bakery import baker
import pytest
from score.models import Score, SCORE_DATE_FIELD_FORMAT
from django.core.cache import cache
from datetime import datetime

User = get_user_model()


@pytest.fixture
def create_score(api_client):
    def do_create_score(score):
        return api_client.post('/score/', score)
    return do_create_score


@pytest.mark.django_db
class TestCreateScore:

    def if_data_is_invalid_returns_400(self, create_score):

        # Act
        response = create_score({'number': -1})

        #  Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['number'] is not None

    def if_number_is_not_provided_return_400(self, create_score):

        # Act
        response = create_score({})

        #  Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    class TestAnonymousUser:

        """
        HAPPY PATHS
        """

        # @pytest.mark.skip
        # def test_date_and_time_fields_are_set(self, create_score, authenticate):
        # check if the following fields are set correctly
        # - date
        # - time
        # - time_updates (this might not set when object is first created)
        # pass
        def test_if_throttle_limit_not_reached_return_200(self, create_score):

            # Arrange
            cache.clear()
            number = 1

            # Act
            response = create_score({'number': number})

            #  Assert
            assert response.status_code == status.HTTP_201_CREATED
            assert response.data['number'] == number
            assert response.data['uuid'] is not None
            assert response.data['date'] is not None
            assert response.data['tokens'] is not None

        def test_if_score_has_correct_relationship_to_user_object(self, create_score):

            # Arrange
            cache.clear()
            number = 1

            # Act
            response = create_score({'number': number})
            access_token_obj = AccessToken(response.data['tokens']['access'])
            user_id = access_token_obj['user_id']
            score = Score.objects.get(
                user_id=user_id, date=datetime.today())

            #  Assert
            assert response.data['number'] == score.number
            assert response.data['uuid'] == score.uuid

        """
        UNHAPPY PATHS
        """

        def test_if_throttle_limit_reached_return_429(self, create_score):

            # Arrange
            cache.clear()
            number = 1

            # # Act
            resOne = create_score({'number': number})
            resTwo = create_score({'number': number})

            #  Assert
            assert resOne.status_code == status.HTTP_201_CREATED
            assert resTwo.status_code == status.HTTP_429_TOO_MANY_REQUESTS

        def test_if_score_number_is_invalid_return_400(self, create_score):

            # Arrange
            cache.clear()

            # Act, Assert
            TestCreateScore.if_number_is_not_provided_return_400(
                self, create_score)

        def test_if_number_is_not_provided_return_400(self, create_score):

            # Arrange
            cache.clear()

            # Act, Assert
            TestCreateScore.if_number_is_not_provided_return_400(
                self, create_score)

    class TestGuestAndDefaultUser:

        """
        HAPPY PATHS
        """

        def test_if_user_is_authenticated_return_200(self, authenticate, create_score):

            # Arrange
            authenticate()
            number = 1

            # Act
            response = create_score({'number': number})

            #  Assert
            assert response.status_code == status.HTTP_201_CREATED
            assert response.data['number'] == number
            assert response.data['uuid'] is not None
            assert response.data['date'] is not None

        def test_if_score_has_correct_relationship_to_user_object(self, authenticate, create_score):

            # Arrange
            user = baker.make(User)
            authenticate(user=user)
            number = 1

            # Act
            response = create_score({'number': number})
            score = Score.objects.get(
                user_id=user.id, date=datetime.today())

            #  Assert
            assert response.status_code == status.HTTP_201_CREATED
            assert response.data['number'] == score.number
            assert response.data['uuid'] == score.uuid
            assert response.data['date'] == score.date.strftime(
                SCORE_DATE_FIELD_FORMAT)
            assert user.id == score.user_id

        """
        UNHAPPY PATHS
        """

        def test_if_score_has_already_been_created_should_return_401(self, authenticate, create_score):

            # Arrange
            authenticate()
            number = 1

            # Act
            resOne = create_score({'number': number})
            resTwo = create_score({'number': number})

            #  Assert
            assert resOne.status_code == status.HTTP_201_CREATED
            assert resTwo.status_code == status.HTTP_401_UNAUTHORIZED

        def test_if_data_is_invalid_returns_400(self, authenticate, create_score):

            # Arrange
            authenticate()

            # Act, Assert
            TestCreateScore.if_data_is_invalid_returns_400(self, create_score)

        def test_if_number_is_not_provided_return_400(self, authenticate, create_score):

            # Arrange
            authenticate()

            # Act, Assert
            TestCreateScore.if_number_is_not_provided_return_400(
                self, create_score)
