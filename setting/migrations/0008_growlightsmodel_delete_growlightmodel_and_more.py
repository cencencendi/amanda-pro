# Generated by Django 4.2.3 on 2023-08-03 04:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0007_remove_wateringschedule_done_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrowlightsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('switch', models.IntegerField(choices=[(0, 'OFF'), (1, 'ON')], default=0)),
                ('first_cycle_start', models.TimeField(default=datetime.time(11, 7, 49, 600122))),
                ('first_cycle_end', models.TimeField(default=datetime.time(11, 7, 49, 600132))),
                ('second_cycle_start', models.TimeField(default=datetime.time(11, 7, 49, 600135))),
                ('second_cycle_end', models.TimeField(default=datetime.time(11, 7, 49, 600138))),
            ],
        ),
        migrations.DeleteModel(
            name='GrowlightModel',
        ),
        migrations.AlterField(
            model_name='wateringschedule',
            name='watering_time',
            field=models.TimeField(default=datetime.time(11, 7, 49, 600511)),
        ),
    ]