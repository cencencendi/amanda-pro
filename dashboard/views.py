"""
Module: dashboard.views

This module contains Django view functions related to the dashboard functionality.

Functions:
- dashboard(request): Renders the dashboard page.
- get_dashboard_data(request): Retrieves and returns sensor data for the dashboard.
- get_location_and_datetime(request): Retrieves and returns the current location and datetime information.
"""
from django.shortcuts import render
from django.http import JsonResponse
import geocoder
from datetime import datetime
from .models import SensorRecord
from setting.models import DosingTargetAndTolerance


def dashboard(request):
    """
    Renders the dashboard page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered dashboard page.
    """
    return render(request, "dashboard.html")


def get_dashboard_data(request):
    """
    Retrieves sensor data and dosing target information for the dashboard.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing sensor data and dosing target information.
    """
    # Get dashboard data from sensor record database
    try:
        data_sensor = SensorRecord.objects.order_by("-pk")[0]  # Get the last row in database
        target_and_tolerance = DosingTargetAndTolerance.objects.order_by("pk")[0]
    except:
        data_sensor = SensorRecord(ec="-", ph="-", do="-", water_temp="-", kwh="-", co2="-")
        target_and_tolerance = DosingTargetAndTolerance(
            ec_target=0, ec_tolerance=0, ph_target=0, ph_tolerance=0
        )
        print("Sensor database has not created yet!")

    sensorValue = {
        "ecValue": data_sensor.ec,
        "pHValue": data_sensor.ph,
        "doValue": data_sensor.do,
        "waterTempValue": data_sensor.water_temp,
        "kWhValue": data_sensor.kwh,
        "co2Value": data_sensor.co2,
    }

    ec_lower = target_and_tolerance.ec_target - target_and_tolerance.ec_tolerance
    ec_upper = target_and_tolerance.ec_target + target_and_tolerance.ec_tolerance
    ph_lower = target_and_tolerance.ph_target - target_and_tolerance.ph_tolerance
    ph_upper = target_and_tolerance.ph_target + target_and_tolerance.ph_tolerance

    sensingCondition = {  # check if ec and ph value is in range between their target and tolerance
        "isECAppropriate": True if (ec_lower) <= data_sensor.ec <= (ec_upper) else False,
        "ispHAppropriate": True if (ph_lower) <= data_sensor.ph <= (ph_upper) else False,
    }

    context = {"sensorValue": sensorValue, "sensingCondition": sensingCondition}
    return JsonResponse(context)


def get_location_and_datetime(request):
    """
    Retrieves the current location and datetime information.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing current location and datetime information.
    """
    location = geocoder.ip("me").city
    now = datetime.now()

    date_format = "%A, %d %B %Y"
    time_format = "%H:%M"

    context = {
        "location": location,
        "date": now.strftime(date_format),
        "time": now.strftime(time_format),
    }

    return JsonResponse(context)
