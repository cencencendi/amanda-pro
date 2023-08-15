import time
from setting.models import DosingTargetAndTolerance, SettingMode, IrrigationModel
from dashboard.models import SensorRecord
from .plc import PLC


class DosingCycle:
    """
    DosingCycle Class
    -----------------

    This class manages the dosing control cycle for an irrigation system based on sensor data and user-defined settings. It checks sensor readings against target values and handles dosing adjustments as needed.

    Attributes:
        insert_sensor_record: An instance of the InsertSensorRecord class for recording sensor data.
        target_and_tolerance (DosingTargetAndTolerance): The model for storing dosing target values and tolerances.
        setting_mode (SettingMode): The model for storing system operation modes.
        irrigation_model (IrrigationModel): The model for storing irrigation-related settings.
        sensor_record (SensorRecord): The model for storing recorded sensor data.
        plc (PLC): An instance of the PLC class for interacting with a PLC device.

    Methods:
        dosing_control(): Initiates the dosing control cycle, determining whether dosing adjustments are needed based on system settings.
        dosing_check(): Checks sensor readings against target values and initiates dosing adjustments if necessary.
        stirring(): Activates the stirring process to ensure nutrient mixing.
        adjust_nutrient(): Adjusts nutrient dosing based on sensor readings and target values.
        get_fresh_water(): Initiates the process of obtaining fresh water if dosing adjustments require it.

    Usage:
        Create an instance of the DosingCycle class, providing the necessary dependencies. Call the dosing_control() method to initiate the dosing control cycle.

    Example:
        insert_sensor_record_instance = InsertSensorRecord(plc_instance, arduino_instance, thermostat_instance)
        dosing_cycle = DosingCycle(insert_sensor_record_instance)
        dosing_cycle.dosing_control()"""

    def __init__(
        self,
        insert_sensor_record,
        plc,
        target_and_tolerance=DosingTargetAndTolerance,
        setting_mode=SettingMode,
        irrigation_model=IrrigationModel,
        sensor_record=SensorRecord,
    ) -> None:
        self.target_and_tolerance = target_and_tolerance
        self.setting_mode = setting_mode
        self.irrigation_model = irrigation_model
        self.insert_sensor_record = insert_sensor_record
        self.sensor_record = sensor_record
        self.plc = plc
        self.is_dosed = False

    def dosing_control(self):
        self.last_target_and_tolerance = self.target_and_tolerance.objects.order_by("-pk")[0]
        self.last_setting_mode = self.setting_mode.objects.order_by("-pk")[0]
        self.last_irrigation_model = self.irrigation_model.objects.order_by("-pk")[0]

        self.is_need_to_be_dosed = (
            self.last_setting_mode.irrigation_mode == 0
            and self.last_irrigation_model.sensor_cycle_switch == 1
        ) or self.last_setting_mode.irrigation_mode == 1

        self.insert_sensor_record.record_time() if self.is_need_to_be_dosed else None
        self.last_sensor_record = self.sensor_record.objects.order_by("-pk")[0]

        if self.is_need_to_be_dosed and self.last_setting_mode.dosing_mode:
            self.dosing_check()

    def dosing_check(self):
        is_water_tank_full = self.plc.read_capacitor(38)

        self.ec_lower = (
            self.last_target_and_tolerance.ec_target - self.last_target_and_tolerance.ec_tolerance
        )
        self.ec_upper = (
            self.last_target_and_tolerance.ec_target + self.last_target_and_tolerance.ec_tolerance
        )
        self.ph_lower = (
            self.last_target_and_tolerance.ph_target - self.last_target_and_tolerance.ph_tolerance
        )
        self.ph_upper = (
            self.last_target_and_tolerance.ph_target + self.last_target_and_tolerance.ph_tolerance
        )

        self.is_dosed = (
            True
            if (
                (self.ph_lower <= self.last_sensor_record.ph <= self.ph_upper)
                and (self.ec_lower <= self.last_sensor_record.ec <= self.ec_upper)
            )
            else False
        )

        if self.is_dosed:
            print("already dosed")
            return

        if not self.is_dosed and is_water_tank_full:
            self.plc.write_plc(id=20, switch=True)
            time.sleep(2)
            self.plc.write_plc(id=20, switch=False)
            return

        # self.stirring()
        self.adjust_nutrient()

    def stirring(self):
        print("stirring")
        self.plc.write_plc(id=8, switch=True)
        self.plc.write_plc(id=9, switch=True)
        time.sleep(5)
        self.plc.write_plc(id=8, switch=False)
        self.plc.write_plc(id=9, switch=False)

    def adjust_nutrient(self):
        is_need_more_water = False
        if self.last_sensor_record.ec < self.ec_lower:
            print("ec too low!")
            self.plc.write_plc(id=4, switch=True, mililiter=100)

        elif self.last_sensor_record.ec > self.ec_upper:
            print("ec too high!")
            is_need_more_water = True

        if self.last_sensor_record.ph < self.ph_lower:
            print("ph too low!")
            is_need_more_water = True

        elif self.last_sensor_record.ph > self.ph_upper:
            print("ph too high!")
            self.plc.write_plc(id=5, switch=True, mililiter=15)

        time.sleep(3)
        self.plc.write_plc(id=4, switch=False)
        self.plc.write_plc(id=5, switch=False)

        if is_need_more_water:
            self.get_fresh_water()

    def get_fresh_water(self):
        print("getting fresh water")
        self.plc.write_plc(id=1, switch=True)
        time.sleep(60)
        self.plc.write_plc(id=1, switch=False)
