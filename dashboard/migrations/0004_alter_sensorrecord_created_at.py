# Generated by Django 4.2.3 on 2023-08-07 02:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0003_alter_sensorrecord_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sensorrecord",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]