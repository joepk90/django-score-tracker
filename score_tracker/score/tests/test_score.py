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


@ pytest.mark.django_db
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
