<<<<<<< HEAD
# Generated by Django 4.2.3 on 2023-08-15 10:47

=======
# Generated by Django 4.2.3 on 2023-08-15 13:49

import datetime
>>>>>>> 30a9380c67f27c4e17fc2c230ccc709d6e7c1d63
from django.db import migrations, models


class Migration(migrations.Migration):
<<<<<<< HEAD

    dependencies = [
        ('dashboard', '0007_alter_sensorrecord_created_at'),
=======
    dependencies = [
        ("dashboard", "0007_alter_sensorrecord_created_at"),
>>>>>>> 30a9380c67f27c4e17fc2c230ccc709d6e7c1d63
    ]

    operations = [
        migrations.AlterField(
<<<<<<< HEAD
            model_name='sensorrecord',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
=======
            model_name="sensorrecord",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 8, 15, 20, 49, 2, 93201)
            ),
>>>>>>> 30a9380c67f27c4e17fc2c230ccc709d6e7c1d63
        ),
    ]
