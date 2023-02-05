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
