"""
Module: growlights.views

This module contains Django view functions related to the growlights functionality.

Functions:
- growlights(request): Renders the growlights page.
- get_growlights_data(request): Retrieves growlights-related data from the database and returns it as a JSON response.
- update_growlights_data(request): Handles updating growlights-related data in the database based on POST requests.
- save_to_database(data): Updates growlights-related data in the database based on input JSON data.
- manual_growlight(growlights_model): Performs manual growlight control based on the provided growlights model.

"""
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from .models import GrowlightsModel, SettingMode
from datetime import datetime
from core.plc import PLC

# Create your views here.

plc = PLC()


def growlights(request):
    """
    Renders the growlights page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered growlights page.
    """
    return render(request, "growlights.html")


def get_growlights_data(request):
    """
    Retrieves growlights-related data from the database and returns it as a JSON response.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing growlights-related data.
    """
    # Get the last row in the SettingMode database (eventhough there is only one row of data :D)
    setting_mode = SettingMode.objects.order_by("pk")[0]

    # Get all row in the GrowlightsModel database
    growlight_model = GrowlightsModel.objects.order_by("pk")

    timeData = []

    for row in growlight_model:
        growlight_time = {
            "firstCycle": {
                "startTime": row.first_cycle_start.strftime("%H:%M"),
                "endTime": row.first_cycle_end.strftime("%H:%M"),
            },
            "secondCycle": {
                "startTime": row.second_cycle_start.strftime("%H:%M"),
                "endTime": row.second_cycle_end.strftime("%H:%M"),
            },
        }
        timeData.append(growlight_time)

    switchesData = {
        "firstSwitch": growlight_model[0].switch,
        "secondSwitch": growlight_model[1].switch,
    }

    growlightMode = setting_mode.growlights_mode

    context = {"timeData": timeData, "switchesData": switchesData, "growlightMode": growlightMode}

    return JsonResponse(context)


def update_growlights_data(request):
    """
    Handles updating growlights-related data in the database based on POST requests.

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
    Updates growlights-related data in the database based on input JSON data.

    Parameters:
        data (dict): JSON data containing growlights-related settings.

    Returns:
        None
    """
    # Get the last row in the SettingMode database (eventhough there is only one row of data :D)
    setting_mode = SettingMode.objects.order_by("pk")[0]

    # Get all row in the GrowlightsModel database
    growlights_model = GrowlightsModel.objects.order_by("pk")

    try:
        setting_mode.growlights_mode = data.get("growlightMode")
        setting_mode.save()

        for idx, row in enumerate(growlights_model):
            timeData = data.get("timeData")
            row.first_cycle_start = datetime.strptime(
                timeData[idx].get("firstCycle").get("startTime"), "%H:%M"
            ).time()
            row.first_cycle_end = datetime.strptime(
                timeData[idx].get("firstCycle").get("endTime"), "%H:%M"
            ).time()
            row.second_cycle_start = datetime.strptime(
                timeData[idx].get("secondCycle").get("startTime"), "%H:%M"
            ).time()
            row.second_cycle_end = datetime.strptime(
                timeData[idx].get("secondCycle").get("endTime"), "%H:%M"
            ).time()
            row.save()

        for row, key in zip(growlights_model, data.get("switchesData")):
            row.switch = data.get("switchesData").get(key)
            row.save()
    except:
        print("Error saving data!")

    if not setting_mode.growlights_mode:
        manual_growlight(growlights_model)


def manual_growlight(growlights_model):
    """
    Performs manual growlight control based on the provided growlights model.

    Parameters:
        growlights_model (list): List of GrowlightsModel instances containing growlight settings.

    Returns:
        None
    """
    # Turn all the growlight on/off
    for idx, row in enumerate(growlights_model):
        plc.write_plc(id=15 + idx, switch=row.switch)
        print(f"Growlight-{idx+1} is {'on' if row.switch else 'off'}!")
