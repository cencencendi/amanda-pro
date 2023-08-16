# Generated by Django 4.2.3 on 2023-08-15 10:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0018_alter_growlightsmodel_first_cycle_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='growlightsmodel',
            name='first_cycle_end',
            field=models.TimeField(default=datetime.time(17, 50, 31, 280055)),
        ),
        migrations.AlterField(
            model_name='growlightsmodel',
            name='first_cycle_start',
            field=models.TimeField(default=datetime.time(17, 50, 31, 280030)),
        ),
        migrations.AlterField(
            model_name='growlightsmodel',
            name='second_cycle_end',
            field=models.TimeField(default=datetime.time(17, 50, 31, 280075)),
        ),
        migrations.AlterField(
            model_name='growlightsmodel',
            name='second_cycle_start',
            field=models.TimeField(default=datetime.time(17, 50, 31, 280065)),
        ),
        migrations.AlterField(
            model_name='wateringschedule',
            name='watering_time',
            field=models.TimeField(default=datetime.time(17, 50, 31, 281798)),
        ),
    ]
