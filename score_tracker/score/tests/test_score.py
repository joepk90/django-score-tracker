from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from model_bakery import baker
import pytest
from score.models import Score, SCORE_DATE_FIELD_FORMAT
from django.core.cache import cache
from datetime import datetime
import uuid

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


@pytest.fixture
def update_score(api_client):
    def do_create_score(uuid, number=1):
        return api_client.put(f'/score/{uuid}/', {'number': number})
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

        @pytest.mark.skip
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


@pytest.mark.django_db
class TestUpdateScore:

    def if_uuid_is_invalid_return_401(self, update_score):

        #  arrange
        scoreUUID = uuid.uuid4()

        # act
        response = update_score(scoreUUID)

        # assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def if_uuid_is_exists_return_401(self, update_score):

        #  arrange
        scoreUUID = ""

        # act
        response = update_score(scoreUUID)

        # assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def if_user_is_anon_return_401(self, update_score):

        #  arrange
        user = baker.make(User)
        score = baker.make(Score, user_id=user.id)

        # act
        response = update_score(score.uuid)

        # assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def if_user_can_update_unnassigned_score_return_401(self, update_score):

        #  arrange
        score = baker.make(Score)

        # act
        response = update_score(score.uuid)

        # assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    class TestAnonymousUser:

        """
        UNHAPPY PATHS
        """

        def test_if_uuid_is_invalid_return_401(self, update_score):
            TestUpdateScore.if_uuid_is_invalid_return_401(self, update_score)

        def test_if_uuid_is_exists_return_401(self, update_score):
            TestUpdateScore.if_uuid_is_exists_return_401(self, update_score)

        def test_if_user_is_anon_return_401(self, update_score):
            TestUpdateScore.if_user_is_anon_return_401(self, update_score)

        def test_if_user_can_update_unnassigned_score_return_401(self, update_score):
            TestUpdateScore.if_user_can_update_unnassigned_score_return_401(
                self, update_score)

    class TestGuestAndDefaultUser:

        """
        HAPPY PATHS
        """

        def test_if_user_updates_score_return_200(self, authenticate, update_score):

            #  arrange
            number = 2
            user = baker.make(User)
            authenticate(user=user)
            score = baker.make(Score, user_id=user.id, number=1)

            # act
            response = update_score(score.uuid, number)

            # assert
            assert response.status_code == status.HTTP_200_OK
            assert response.data['number'] == number

        def test_if_updating_score_updating_time_updated_field(self, authenticate, update_score):
            #  arrange
            number = 2
            user = baker.make(User)
            authenticate(user=user)
            score = baker.make(Score, user_id=user.id, number=1)

            # act
            update_score(score.uuid, number)

            # assert
            scoreUpdate = Score.objects.get(
                user_id=user.id, date=datetime.today())
            assert scoreUpdate.time_updated > score.time_updated

        """
        UNHAPPY PATHS
        """
        @pytest.mark.skip
        def test_if_score_does_not_exist_return_200(self, authenticate, create_score):
            pass

        @pytest.mark.skip
        def test_if_data_is_invalid_returns_400(self, authenticate, create_score):

            # Arrange
            authenticate()

            # Act, Assert
            # if_data_is_invalid_returns_400(self, create_score)

        @pytest.mark.skip
        def test_if_number_is_not_provided_return_400(self, authenticate, create_score):

            # Arrange
            authenticate()

            # Act, Assert
            # if_number_is_not_provided_return_400(self, create_score)


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
