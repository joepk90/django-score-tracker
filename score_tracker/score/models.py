from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Score(models.Model):
    number = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10)
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
