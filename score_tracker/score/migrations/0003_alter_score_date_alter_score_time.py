# Generated by Django 4.0 on 2023-01-14 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0002_score_time_score_time_updated_alter_score_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
