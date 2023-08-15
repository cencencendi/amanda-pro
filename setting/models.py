from django.db import models
from django.utils import timezone

# Create your models here.

MODE_STATE = ((1, "AUTO"), (0, "MANUAL"))
BUTTON_STATE = ((0, "OFF"), (1, "ON"))

DONE_STATE = ((0, "NOT DONE"), (1, "DONE"))

# ================================================== Setting Mode ================================================


class SettingMode(models.Model):
    growlights_mode = models.IntegerField(choices=MODE_STATE, default=1)
    irrigation_mode = models.IntegerField(choices=MODE_STATE, default=1)
    dosing_mode = models.IntegerField(choices=MODE_STATE, default=1)


# ========================================= Growlight Model (Times and Switches) ================================================
"""
Growlight 1: is the Object 1 or Row 1 in the database 
Growlight 2: is the Object 2 or Row 2 in the database
"""


class GrowlightsModel(models.Model):
    switch = models.IntegerField(choices=BUTTON_STATE, default=0)
    first_cycle_start = models.TimeField(default=timezone.now().time)
    first_cycle_end = models.TimeField(default=timezone.now().time)
    second_cycle_start = models.TimeField(default=timezone.now().time)
    second_cycle_end = models.TimeField(default=timezone.now().time)


# ============================================== Irrigation Model (Switches) ===================================================


class IrrigationModel(models.Model):
    water_supply_switch = models.IntegerField(choices=BUTTON_STATE, default=0)
    sensor_pump_switch = models.IntegerField(choices=BUTTON_STATE, default=0)
    plant_pump_switch = models.IntegerField(choices=BUTTON_STATE, default=0)
    drain_valve_switch = models.IntegerField(choices=BUTTON_STATE, default=0)
    sensor_cycle_switch = models.IntegerField(choices=BUTTON_STATE, default=0)


# ============================================== Dosing Model (Schedules and Switches) ===================================================
"""
The dosing model database will be divided into 2 different classes:
1. DosingTargetAndTolerance
2. DosingSwitches
3. WateringSchedule
"""


class DosingTargetAndTolerance(models.Model):
    ec_target = models.IntegerField(default=1800)
    ec_tolerance = models.IntegerField(default=0)
    ph_target = models.FloatField(default=6.0)
    ph_tolerance = models.FloatField(default=0.0)


class DosingSwitches(models.Model):
    ec_switch = models.IntegerField(choices=BUTTON_STATE, default=0)
    ph_switch = models.IntegerField(choices=BUTTON_STATE, default=0)


class WateringSchedule(models.Model):
    name = models.TextField(null=True, max_length=15)
    watering_time = models.TimeField(default=timezone.now().time)
    duration = models.IntegerField(default=0)
