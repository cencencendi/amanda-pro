from setting.models import WateringSchedule
from .plc import PLC
import time
from datetime import datetime, timedelta


class Watering:
    """
    Watering Class
    --------------

    This class manages the watering schedule in an automated irrigation system. It checks the current time against predefined watering schedules and triggers watering if conditions are met.

    Attributes:
        plc (PLC): An instance of the PLC class for controlling the irrigation system.
        watering_schedule (WateringSchedule): The model for storing watering schedules.

    Methods:
        __init__(): Initializes the Watering class by providing necessary dependencies.
        check_time(dosing_cycle): Continuously checks the current time against watering schedules and initiates watering if conditions are met.
        time_to_watering(): Initiates the watering process based on the identified watering time and duration.
        is_between(start, end, now): Checks if the current time is within a specified time range.

    Usage:
        Create an instance of the Watering class, providing the required dependencies. Call the check_time() method to continuously monitor watering schedules and trigger watering as necessary.

    Example:
        plc_instance = PLC()
        watering_instance = Watering(plc_instance)
        watering_instance.check_time(dosing_cycle_instance)"""

    def __init__(self, plc, watering_schedule=WateringSchedule) -> None:
        self.watering_schedule = watering_schedule
        self.plc = plc
        self.is_now_between_schedule = []

    def check_time(self, dosing_cycle):
        while True:  # Because we will use python package called threading
            self.now = datetime.now().time()
            self.time_and_duration = self.watering_schedule.objects.order_by("pk")
            time.sleep(5)

            if not dosing_cycle.is_dosed:
                continue

            for row in self.time_and_duration:
                end_time_of_schedule = (
                    datetime.combine(datetime.min, row.watering_time)
                    + timedelta(minutes=row.duration)
                ).time()  # If watering_time is 12:35 with duration 2 minutes, then end_time_of_schedule is 12:37
                self.is_now_between_schedule.append(
                    (
                        self.is_between(row.watering_time, end_time_of_schedule, self.now),
                        row.watering_time,
                        row.duration,
                    )  # self.is_now_between_schedule = [(False, 12:35, 2), (True, 16:00, 3), etc]
                )
            if any(
                item[0] for item in self.is_now_between_schedule
            ):  # Check for any "True" in the list
                self.time_to_watering()

    def time_to_watering(self):

        # get the watering_time and duration
        watering_time = next(item[1] for item in self.is_now_between_schedule if item[0])
        watering_duration = next(item[2] for item in self.is_now_between_schedule if item[0])

        print(f"watering time: {watering_time} duration: {watering_duration}")
        # self.plc.write_plc(id=2,switch=True)
        time.sleep(watering_duration * 60)

        print(f"done watering at: {datetime.now().time()}")
        # self.plc.write_plc(id=2,switch=False)
        self.is_now_between_schedule.clear()

    def is_between(self, start, end, now):
        is_between = False
        is_between |= start <= now <= end
        is_between |= end < start and (start <= now or now <= end)
        return is_between
