# Generated by Django 4.2.3 on 2023-07-31 09:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DosingSwtiches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ec_switch', models.IntegerField(choices=[(0, 'OFF'), (1, 'ON')], default=0)),
                ('ph_switch', models.IntegerField(choices=[(0, 'OFF'), (1, 'ON')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DosingTargetAndTolerance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ec_target', models.IntegerField(default=1800)),
                ('ec_tolerance', models.IntegerField(default=0)),
                ('ph_target', models.DecimalField(decimal_places=2, default=6.0, max_digits=4)),
                ('ph_tolerance', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='GrowlightModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('switch', models.IntegerField(choices=[(0, 'OFF'), (1, 'ON')], default=0)),
                ('first_cycle_start', models.TimeField(default=django.utils.timezone.now)),
                ('first_cycle_end', models.TimeField(default=django.utils.timezone.now)),
                ('second_cycle_start', models.TimeField(default=django.utils.timezone.now)),
                ('second_cycle_end', models.TimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='IrrigationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('water_supply_switch', models.IntegerField(choices=[(0, 'OFF'), (1, 'ON')], default=0)),
                ('sensor_pump_switch', models.IntegerField(choices=[(0, 'OFF'), (1, 'ON')], default=0)),
                ('plant_pump_switch', models.IntegerField(choices=[(0, 'OFF'), (1, 'ON')], default=0)),
                ('drain_valve_switch', models.IntegerField(choices=[(0, 'OFF'), (1, 'ON')], default=0)),
                ('sensor_cycle_switch', models.IntegerField(choices=[(0, 'OFF'), (1, 'ON')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SettingMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('growlight_mode', models.IntegerField(choices=[(1, 'AUTO'), (0, 'MANUAL')], default=1)),
                ('irrigation_mode', models.IntegerField(choices=[(1, 'AUTO'), (0, 'MANUAL')], default=1)),
                ('dosing_mode', models.IntegerField(choices=[(1, 'AUTO'), (0, 'MANUAL')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='WateringSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=15, null=True)),
                ('watering_time', models.DateTimeField(null=True)),
                ('done', models.IntegerField(choices=[(0, 'NOT DONE'), (1, 'DONE')], default=0)),
            ],
        ),
    ]