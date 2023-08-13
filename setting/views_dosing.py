"""
Module: dosing.views

This module contains Django view functions related to the dosing functionality.

Functions:
- dosing(request): Renders the dosing page.
- get_dosing_data(request): Retrieves dosing-related data from the database and returns it as a JSON response.
- update_dosing_data(request): Handles updating dosing-related data in the database based on POST requests.
- save_to_database(data): Updates dosing-related data in the database based on input JSON data.
- manual_dosing(switches): Performs manual dosing control based on the provided switch settings.
"""
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from .models import SettingMode, DosingTargetAndTolerance, DosingSwitches, WateringSchedule
from datetime import datetime
from core.plc import PLC
import time

# Create your views here.

plc = PLC()


def dosing(request):
    """
    Renders the dosing page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered dosing page.
    """
    return render(request, "dosing.html")


def get_dosing_data(request):
    """
    Retrieves dosing-related data from the database and returns it as a JSON response.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing dosing-related data.
    """
    # Get the last row in the SettingMode database (eventhough there is only one row of data :D)
    setting_mode = SettingMode.objects.order_by("pk")[0]

    # Get all row in the DosingTargetAndTolerance, DosingSwitches, and WateringSchedule database
    target_and_tolerance = DosingTargetAndTolerance.objects.order_by("pk")[0]
    switches = DosingSwitches.objects.order_by("pk")[0]
    watering_schedule = WateringSchedule.objects.order_by("pk")

    context = {
        "dosingControlMode": setting_mode.dosing_mode,
        "targetAndTolerance": {
            "ec-target": target_and_tolerance.ec_target,
            "ec-tolerance": target_and_tolerance.ec_tolerance,
            "ph-target": target_and_tolerance.ph_target,
            "ph-tolerance": target_and_tolerance.ph_tolerance,
        },
        "dosingSwitches": {"ec-switch": switches.ec_switch, "ph-switch": switches.ph_switch},
        "wateringSchedule": [
            {
                "time": schedule.watering_time.strftime("%H:%M"),
                "duration": schedule.duration,
            }
            for schedule in watering_schedule
        ],
    }
    return JsonResponse(context)


def update_dosing_data(request):
    """
    Handles updating dosing-related data in the database based on POST requests.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response confirming the update.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            save_to_database(data)
            return JsonResponse({"message": "Data updated successfully"})
        except json.JSONDecodeError:
            # Return an error response if the JSON data is not valid
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    else:
        # Return an error response if the request method is not POST
        return HttpResponse(status=405)


# Save data to database
def save_to_database(data):
    """
    Updates dosing-related data in the database based on input JSON data.

    Parameters:
        data (dict): JSON data containing dosing-related settings.

    Returns:
        None
    """
    # Get the last row in the SettingMode database (eventhough there is only one row of data :D)
    setting_mode = SettingMode.objects.order_by("pk")[0]

    # Get all row in the DosingTargetAndTolerance, DosingSwitches, and WateringSchedule database
    target_and_tolerance = DosingTargetAndTolerance.objects.order_by("pk")[0]
    switches = DosingSwitches.objects.order_by("pk")[0]
    WateringSchedule.objects.all().delete()
    try:
        setting_mode.dosing_mode = data.get("dosingMode")
        setting_mode.save()

        for key, value in data.get("targetAndTolerance").items():
            setattr(target_and_tolerance, key, value)
        target_and_tolerance.save()

        for key, value in data.get("dosingSwitches").items():
            setattr(switches, key, value)
        switches.save()

        for idx, schedules in enumerate(data.get("wateringSchedule")):
            watering_schedule = WateringSchedule(
                id=idx + 1,
                name=f"Schedule {idx+1}",
                watering_time=datetime.strptime(schedules.get("time"), "%H:%M").time(),
                duration=int(schedules.get("duration")),
            )
            watering_schedule.save()
    except:
        print("Error saving data!")

    if not setting_mode.dosing_mode:
        manual_dosing(switches)


def manual_dosing(switches):
    """
    Performs manual dosing control based on the provided switch settings.

    Parameters:
        switches (DosingSwitches): Dosing switches object containing switch settings.

    Returns:
        None
    """

    # Turn EC switch on/off
    def ec_stirrer():
        plc.write_plc(id=8, switch=True)
        time.sleep(5)
        plc.write_plc(id=8, switch=False)

    ec_stirrer() if switches.ec_switch else None
    plc.write_plc(id=13, switch=switches.ec_switch)
    print(f'EC switch and stirer {"on" if switches.ec_switch else "off"}')

    # Turn ph switch on/off

    def ph_stirrer():
        plc.write_plc(id=9, switch=True)
        time.sleep(5)
        plc.write_plc(id=9, switch=False)

    ph_stirrer() if switches.ph_switch else None
    plc.write_plc(id=14, switch=switches.ph_switch)
    print(f'pH switch and stirer {"on" if switches.ph_switch else "off"}')
