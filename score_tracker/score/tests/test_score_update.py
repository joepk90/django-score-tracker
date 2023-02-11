from django.contrib.auth import get_user_model
from rest_framework import status
from model_bakery import baker
import pytest
from datetime import datetime, date
import uuid
from score.models import Score

User = get_user_model()


@pytest.mark.django_db
class TestUpdateScore:

    def if_uuid_does_not_exists_return_401(self, update_score):

        #  arrange
        scoreUUID = uuid.uuid4()
        number = 1

        # act
        response = update_score(scoreUUID, {"number": number})

        # assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def if_uuid_is_invalid_return_401(self, update_score):

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
        return update_score(score.uuid, {"number": number})

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

            # Act, Arrange, Assert
            TestUpdateScore.if_uuid_is_invalid_return_401(self, update_score)

        def test_if_uuid_does_not_exists_return_401(self, update_score):

            # Act, Arrange, Assert
            TestUpdateScore.if_uuid_does_not_exists_return_401(
                self, update_score)

        def test_if_user_is_anon_return_401(self, update_score):

            # Act, Arrange, Assert
            TestUpdateScore.if_user_is_anon_return_401(self, update_score)

        def test_if_user_can_update_unnassigned_score_return_401(self, update_score):

            # Act, Arrange
            response = TestUpdateScore.if_user_can_update_unnassigned_score_return_401(
                self, update_score)

            # Assert
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

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
            TestUpdateScore.if_uuid_does_not_exists_return_401(
                self, update_score)

        def test_if_uuid_is_invalid_return_401(self, authenticate, update_score):

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

        def test_if_user_can_update_unnassigned_score_return_401(self, authenticate, update_score):

            # Arrange
            authenticate()

            # Act
            response = TestUpdateScore.if_user_can_update_unnassigned_score_return_401(
                self, update_score)

            # Assert
            assert response.status_code == status.HTTP_403_FORBIDDEN

        def test_if_user_can_update_score_created_before_today_return_401(self, authenticate, update_score):

            # Arrange
            number = 3
            my_date = date(1970, 1, 1)

            user = baker.make(User)
            authenticate(user=user)
            score = baker.make(Score, user_id=user.id, number=1)

            # update date (not possible on object creation: https://code.djangoproject.com/ticket/16583)
            Score.objects.filter(
                uuid=score.uuid).update(date=my_date)

            # act
            response = update_score(score.uuid, {"number": number})

            # Assert
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
