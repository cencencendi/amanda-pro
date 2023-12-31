# Generated by Django 4.2.3 on 2023-08-07 10:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("setting", "0013_alter_growlightsmodel_first_cycle_end_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="growlightsmodel",
            name="first_cycle_end",
            field=models.TimeField(default=datetime.time(10, 9, 31, 587602)),
        ),
        migrations.AlterField(
            model_name="growlightsmodel",
            name="first_cycle_start",
            field=models.TimeField(default=datetime.time(10, 9, 31, 587589)),
        ),
        migrations.AlterField(
            model_name="growlightsmodel",
            name="second_cycle_end",
            field=models.TimeField(default=datetime.time(10, 9, 31, 587608)),
        ),
        migrations.AlterField(
            model_name="growlightsmodel",
            name="second_cycle_start",
            field=models.TimeField(default=datetime.time(10, 9, 31, 587605)),
        ),
        migrations.AlterField(
            model_name="wateringschedule",
            name="watering_time",
            field=models.TimeField(default=datetime.time(10, 9, 31, 587972)),
        ),
    ]
