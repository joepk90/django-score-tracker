from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from model_bakery import baker
import pytest
from score.models import Score, SCORE_DATE_FIELD_FORMAT
from django.core.cache import cache
from datetime import datetime


# baker will dynamically create objects (including model relationships)

# make db connection
# @pytest.mark.django_db

# skip test
# @pytest.mark.skip

# test format
# Arrange, Act, Assert

User = get_user_model()


@pytest.fixture
def create_score(api_client):
    def do_create_score(score):
        return api_client.post('/score/', score)
    return do_create_score


def if_data_is_invalid_returns_400(self, create_score):
    # Act
    response = create_score({'number': -1})

    #  Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['number'] is not None


@pytest.mark.django_db
class TestCreateScore:

    # should fail if number is invalid
    # should fail if user has already created a score

    class TestAnonymousUser:

        # happy paths
        def test_if_throttle_limit_not_reached_return_200(self, create_score, authenticate):

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

        def test_if_score_has_correct_user_relationship(self, create_score):

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

        # unhappy paths
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
            number = -1

            # # Act
            response = create_score({'number': number})

            #  Assert
            assert response.status_code == status.HTTP_400_BAD_REQUEST

        def test_if_score_number_is_provided_return_400(self, create_score):

            # Arrange
            cache.clear()

            # # Act
            response = create_score({})

            #  Assert
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    class TestGuestAndDefaultUser:

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

        def test_if_data_is_invalid_returns_400(self, authenticate, create_score):

            # Arrange
            authenticate()

            # Act, Assert
            if_data_is_invalid_returns_400(self, create_score)

        def test_if_data_is_valid_returns_201(self, api_client):

            # Arrange
            api_client.force_authenticate(user=User())

            # Act
            response = api_client.post('/score/', {
                'number': 1
            })

            #  Assert
            assert response.status_code == status.HTTP_201_CREATED
            assert response.data['number'] == 1


@pytest.mark.django_db
class TestGuestCreateScore:
    def test_if_user_is_anon_return_200(self, create_score, authenticate):

        # Arrange
        user = baker.make(User, is_guest=True)
        authenticate(user=user)
        number = 1

        # Act
        response = create_score({'number': number})

        print("response.status_code", response.status_code)

        #  Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['number'] == number

    def test_if_user_is_anon_and_makes_multiple_requests_return_200(self, create_score, authenticate):

        # Arrange
        user = baker.make(User, is_guest=True)
        authenticate(user=user)
        number = 1

        # Act
        resOne = create_score({'number': number})
        resTwo = create_score({'number': number})

        #  Assert
        assert resOne.status_code == status.HTTP_201_CREATED
        assert resTwo.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestRetreiveScore:
    def test_if_score_exists_return_200(self, api_client, authenticate):

        # Arrange
        # Score.objects.create(number=5)
        # score = baker.make(Score, _quantity=10) # create 10 score objects
        user = baker.make(User)
        authenticate(user=user)
        score = baker.make(Score, user_id=user.id)  #  populate the user field

        # Act
        response = api_client.get(f'/score/{score.uuid}/')

        # Assert
        assert response.status_code == status.HTTP_200_OK

        # concerned this assertion may be too brittle...
        assert response.data == {
            'uuid': score.uuid,
            'number': score.number,
            'date': score.date.strftime(SCORE_DATE_FIELD_FORMAT)
        }
