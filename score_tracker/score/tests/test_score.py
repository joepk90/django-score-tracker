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
def update_score(api_client):
    def update_score(uuid, data):
        return api_client.put(f'/score/{uuid}/', data)
    return update_score


@pytest.mark.django_db
class TestUpdateScore:

    def if_uuid_is_invalid_return_401(self, update_score):

        #  arrange
        scoreUUID = uuid.uuid4()
        number = 1

        # act
        response = update_score(scoreUUID, {"number": number})

        # assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def if_uuid_is_exists_return_401(self, update_score):

        #  arrange
        scoreUUID = ""
        number = 1

        # act
        response = update_score(scoreUUID, {"number": number})

        # assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def if_user_is_anon_return_401(self, update_score):

        #  arrange
        user = baker.make(User)
        score = baker.make(Score, user_id=user.id)
        number = 1

        # act
        response = update_score(score.uuid, {"number": number})

        # assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def if_user_can_update_unnassigned_score_return_401(self, update_score):

        #  arrange
        score = baker.make(Score)
        number = 1

        # act
        response = update_score(score.uuid, {"number": number})

        # assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def if_data_is_invalid_returns_400(self, update_score, user=None):

        # Arrange
        if user == None:
            user = baker.make(User)

        user_id = user.id
        score = baker.make(Score, user_id=user_id)
        number = -1

        # Act
        response = update_score(score.uuid, {"number": number})

        #  Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def if_number_is_not_provided_return_400(self, update_score, user=None):

        # Arrange
        if user == None:
            user = baker.make(User)

        user_id = user.id
        score = baker.make(Score, user_id=user_id)

        # Act
        response = update_score(score.uuid, {})

        #  Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

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
            response = update_score(score.uuid, {"number": number})

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
            update_score(score.uuid, {"number": number})

            # assert
            scoreUpdate = Score.objects.get(
                user_id=user.id, date=datetime.today())
            assert scoreUpdate.time_updated > score.time_updated

        """
        UNHAPPY PATHS
        """

        def test_if_score_does_not_exist_return_200(self, authenticate, update_score):

            # Arrange
            authenticate()

            # Act, Assert
            TestUpdateScore.if_uuid_is_invalid_return_401(self, update_score)

        def if_score_exists_but_data_is_invalid_returns_400(self, authenticate, update_score):

            # Arrange
            user = baker.make(User)
            authenticate(user=user)

            # Act, Assert
            TestUpdateScore.if_data_is_invalid_returns_400(
                self, update_score)

        def test_score_exists_but_number_is_not_provided_return_400(self, authenticate, update_score):

            # Arrange
            user = baker.make(User)
            authenticate(user=user)

            # Act, Assert
            TestUpdateScore.if_number_is_not_provided_return_400(
                self, update_score, user)

        @pytest.mark.skip
        def test_if_uuid_is_invalid_return_401(self, update_score):
            TestUpdateScore.if_uuid_is_invalid_return_401(self, update_score)

        @pytest.mark.skip
        def test_if_uuid_is_exists_return_401(self, update_score):
            TestUpdateScore.if_uuid_is_exists_return_401(self, update_score)

        @pytest.mark.skip
        def test_if_user_can_update_unnassigned_score_return_401(self, update_score):
            TestUpdateScore.if_user_can_update_unnassigned_score_return_401(
                self, update_score)

        @pytest.mark.skip
        def test_if_user_can_update_score_created_before_today_return_401(self, update_score):
            pass


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
