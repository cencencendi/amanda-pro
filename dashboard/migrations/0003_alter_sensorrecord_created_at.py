# Generated by Django 4.2.3 on 2023-08-07 02:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0002_alter_sensorrecord_co2_alter_sensorrecord_do_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sensorrecord",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 8, 7, 9, 42, 51, 35364)
            ),
        ),
    ]
