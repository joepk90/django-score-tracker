# Generated by Django 4.0 on 2023-02-11 17:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0006_alter_score_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='number',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)]),
        ),
    ]