from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from shortuuid.django_fields import ShortUUIDField
from decimal import Decimal

# TODO get dynamically from django defaults...
SCORE_DATE_FIELD_FORMAT = '%Y-%m-%d'

# function can be used to to convert an interger (999) into a decimal with 2 placements (9.99)
# def convert_int_to_decimal(number):
#     return format(number, '.2f')

# NUMBER FIELD STRATEGY
# - save the number as a positive int
# - cover number to decimal when neccessary (maybe only required in the client)
# https://stackoverflow.com/questions/2569015/django-floatfield-or-decimalfield-for-currency#answer-50376841


class Score(models.Model):
    uuid = ShortUUIDField(length=32)
    number = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(1000)
    ])
    # TODO update date time options?
    date = models.DateField(auto_now_add=True)  # date should never change
    time = models.TimeField(auto_now_add=True)
    time_updated = models.TimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    # city = models.CharField(max_length=255) # TODO - extract from IP
    # regio/n = models.CharField(max_length=255) # TODO - extract from IP
    # country = models.CharField(max_length=255) # TODO - extract from IP
