# Generated by Django 4.0 on 2023-01-14 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='time',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='score',
            name='time_updated',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]