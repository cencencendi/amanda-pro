# Generated by Django 4.2.3 on 2023-08-07 03:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0004_alter_sensorrecord_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sensorrecord",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 8, 7, 10, 2, 56, 56072)
            ),
        ),
    ]
