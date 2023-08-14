from datetime import datetime
from setting.models import SettingMode, GrowlightsModel
from .plc import PLC


class GrowlightsControl:
    """
    GrowlightsControl Class
    -----------------------

    This class manages the control of growlights in an automated growth system based on predefined schedules and user settings. It checks the current time against the defined schedules to determine whether the growlights should be turned on or off.

    Attributes:
        plc (PLC): An instance of the PLC class for controlling the growlights.
        growlights_model_database (GrowlightsModel): The model for storing growlight schedules.
        setting_mode (SettingMode): The model for storing system operation modes.

    Methods:
        __init__(): Initializes the GrowlightsControl class by providing necessary dependencies.
        control(): Manages the operation of growlights based on defined schedules and system mode.
        is_between(start, end, now): Checks if the current time is within a specified time range.

    Usage:
        Create an instance of the GrowlightsControl class, providing the required dependencies. Call the control() method to manage the operation of the growlights based on the defined schedules and system mode.

    Example:
        plc_instance = PLC()
        growlights_controller = GrowlightsControl(plc_instance)
        growlights_controller.control()"""

    def __init__(
        self,
        plc,
        growlights_model_database=GrowlightsModel,
        setting_mode=SettingMode,
    ) -> None:
        self.growlights_model_database = growlights_model_database
        self.setting_mode = setting_mode
        self.plc = plc

    def control(self):
        self.growlights_model = self.growlights_model_database.objects.all()
        self.growlights_mode = self.setting_mode.objects.order_by("-pk")[0].growlights_mode

        if self.growlights_mode == False:  # If growlight in manual mode then skip this function
            return

        self.now = datetime.now().time()

        for idx, row in enumerate(self.growlights_model):
            is_now_between_schedule = self.is_between(
                row.first_cycle_start, row.first_cycle_end, self.now
            ) or self.is_between(row.second_cycle_start, row.second_cycle_end, self.now)
            # print(f'Growlight-{idx} is {"on" if is_now_between_schedule else "off"}')
            self.plc.write_plc(id=15 + idx, switch=is_now_between_schedule)

    def is_between(self, start, end, now):
        is_between = False
        is_between |= start <= now <= end
        is_between |= end < start and (start <= now or now <= end)
        return is_between
