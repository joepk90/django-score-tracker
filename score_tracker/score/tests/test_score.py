from django.contrib.auth import get_user_model
from rest_framework import status
from model_bakery import baker
import pytest
from score.models import Score, SCORE_DATE_FIELD_FORMAT
from datetime import datetime, date
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
def get_score(api_client):
    def do_get_score(uuid):
        return api_client.get(f'/score/{uuid}/')
    return do_get_score


@ pytest.mark.django_db
class TestRetreiveScore:

    class TestAnonymousUser:

        """
        UNHAPPY PATHS
        """

        def test_if_anon_user_requests_score_return_401(self, get_score):

            # Arrange
            score = baker.make(Score)  #  populate the user field

            # Act
            response = get_score(score.uuid)

            # Assert
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

    class TestGuestAndDefaultUser:

        """
        HAPPY PATHS
        """

        def test_if_score_exists_return_200(self, get_score, authenticate):

            # Arrange
            # Score.objects.create(number=5)
            # score = baker.make(Score, _quantity=10) # create 10 score objects
            user = baker.make(User)
            authenticate(user=user)
            #  populate the user field
            score = baker.make(Score, user_id=user.id)

            # Act
            response = get_score(score.uuid)

            # Assert
            assert response.status_code == status.HTTP_200_OK

            # concerned this assertion may be too brittle...
            assert response.data == {
                'uuid': score.uuid,
                'number': score.number,
                'date': score.date.strftime(SCORE_DATE_FIELD_FORMAT)
            }
