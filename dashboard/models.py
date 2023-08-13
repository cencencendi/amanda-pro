from django.db import models

# Create your models here.


class SensorRecord(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    ec = models.IntegerField(default=0)
    ph = models.FloatField(default=0)
    water_temp = models.FloatField(default=0)
    do = models.FloatField(default=0)
    co2 = models.IntegerField(default=0)
    kwh = models.IntegerField(default=0)
