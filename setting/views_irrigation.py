"""
Module: irrigation.views

This module contains Django view functions related to the irrigation functionality.

Functions:
- irrigation(request): Renders the irrigation page.
- get_irrigation_data(request): Retrieves irrigation-related data from the database and returns it as a JSON response.
- update_irrigation_data(request): Handles updating irrigation-related data in the database based on POST requests.
- save_to_database(data): Updates irrigation-related data in the database based on input JSON data.
- manual_irrigation(irrigation_model): Performs manual irrigation control based on the provided irrigation model.

"""
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from .models import IrrigationModel, SettingMode
from core.plc import PLC

# Create your views here.

plc = PLC()


def irrigation(request):
    """
    Renders the irrigation page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered irrigation page.
    """
    return render(request, "irrigation.html")


def get_irrigation_data(request):
    """
    Retrieves irrigation-related data from the database and returns it as a JSON response.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing irrigation-related data.
    """
    # Get the last row in the SettingMode database (eventhough there is only one row of data :D)
    setting_mode = SettingMode.objects.order_by("pk")[0]

    # Get all row in the IrrigationModel database
    irrigation_model = IrrigationModel.objects.order_by("pk")[0]

    irrigation_switches = {
        "waterSupplySwitch": irrigation_model.water_supply_switch,
        "sensorPumpSwitch": irrigation_model.sensor_pump_switch,
        "plantPumpSwitch": irrigation_model.plant_pump_switch,
        "drainValveSwitch": irrigation_model.drain_valve_switch,
    }

    context = {
        "irrigationControlMode": setting_mode.irrigation_mode,
        "irrigationControlSwitches": irrigation_switches,
        "sensorCycleSwitch": irrigation_model.sensor_cycle_switch,
    }

    return JsonResponse(context)


def update_irrigation_data(request):
    """
    Handles updating irrigation-related data in the database based on POST requests.

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


def save_to_database(data):
    """
    Updates irrigation-related data in the database based on input JSON data.

    Parameters:
        data (dict): JSON data containing irrigation-related settings.

    Returns:
        None
    """
    # Get the last row in the SettingMode database (eventhough there is only one row of data :D)
    setting_mode = SettingMode.objects.order_by("pk")[0]

    # Get all row in the GrowlightModel database
    irrigation_model = IrrigationModel.objects.order_by("pk")[0]
    try:
        setting_mode.irrigation_mode = data.get("irrigationMode")
        setting_mode.save()

        irrigation_model.water_supply_switch = data.get("irrigationControlSwitches").get(
            "waterSupplySwitch"
        )
        irrigation_model.sensor_pump_switch = data.get("irrigationControlSwitches").get(
            "sensorPumpSwitch"
        )
        irrigation_model.plant_pump_switch = data.get("irrigationControlSwitches").get(
            "plantPumpSwitch"
        )
        irrigation_model.drain_valve_switch = data.get("irrigationControlSwitches").get(
            "drainValveSwitch"
        )

        irrigation_model.sensor_cycle_switch = data.get("sensorCycleSwitch")

        irrigation_model.save()

    except:
        print("error")

    if not setting_mode.irrigation_mode:
        manual_irrigation(irrigation_model)


def manual_irrigation(irrigation_model):
    """
    Performs manual irrigation control based on the provided irrigation model.

    Parameters:
        irrigation_model (IrrigationModel): IrrigationModel instance containing irrigation settings.

    Returns:
        None
    """
    # Turn Water Supply Switch on/off
    plc.write_plc(id=1, switch=irrigation_model.water_supply_switch)
    print(
        f"Water Supply Switch is \
            {'on' if irrigation_model.water_supply_switch else 'off'}!"
    )

    # Turn Sensor Pump Switch on/off
    plc.write_plc(id=3, switch=irrigation_model.sensor_pump_switch)
    print(
        f"Sensor Pump Switch is \
            {'on' if irrigation_model.sensor_pump_switch else 'off'}!"
    )

    # Turn Plant Pump Switch on/off
    plc.write_plc(id=2, switch=irrigation_model.plant_pump_switch)
    print(
        f"Plant Pump Switch is \
            {'on' if irrigation_model.plant_pump_switch else 'off'}!"
    )

    # Turn Drain Valve Switch on/off
    plc.write_plc(id=20, switch=irrigation_model.drain_valve_switch)
    print(
        f"Drain Valve Switch is \
            {'on' if irrigation_model.drain_valve_switch else 'off'}!"
    )
