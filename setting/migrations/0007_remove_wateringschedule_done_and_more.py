# Generated by Django 4.2.3 on 2023-08-02 08:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0006_alter_dosingtargetandtolerance_ph_target_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wateringschedule',
            name='done',
        ),
        migrations.AlterField(
            model_name='growlightmodel',
            name='first_cycle_end',
            field=models.TimeField(default=datetime.time(15, 0, 57, 314660)),
        ),
        migrations.AlterField(
            model_name='growlightmodel',
            name='first_cycle_start',
            field=models.TimeField(default=datetime.time(15, 0, 57, 314650)),
        ),
        migrations.AlterField(
            model_name='growlightmodel',
            name='second_cycle_end',
            field=models.TimeField(default=datetime.time(15, 0, 57, 314666)),
        ),
        migrations.AlterField(
            model_name='growlightmodel',
            name='second_cycle_start',
            field=models.TimeField(default=datetime.time(15, 0, 57, 314664)),
        ),
        migrations.AlterField(
            model_name='wateringschedule',
            name='watering_time',
            field=models.TimeField(default=datetime.time(15, 0, 57, 315026)),
        ),
    ]