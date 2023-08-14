from datetime import datetime
from dashboard.models import SensorRecord
from core.getAPIdata import get_data_co2
import time
import random


class InsertSensorRecord:
    """
    InsertSensorRecord Class
    ------------------------

    This class is responsible for recording sensor data from various sources and saving it to a database. It retrieves data from a water sensing system controlled by a PLC, an Arduino, and a Thera energy meter. The recorded data includes parameters like electrical conductivity (EC), pH, dissolved oxygen (DO), water temperature, kilowatt-hour (kWh) usage, and carbon dioxide (CO2) concentration.

    Attributes:
        plc (PLC): An instance of the PLC class for controlling the water sensing system.
        arduino (Arduino): An instance of the Arduino class for retrieving sensor data.
        thera (Thera): An instance of the Thera class for obtaining energy consumption data.
        sensing_time (int): The duration (in seconds) for which the sensors are active during each sensing cycle.

    Methods:
        record_time(): Initiates the sensor recording process, collects data from various sources, saves the data to the database, and returns the recorded data.

    Usage:
        Create an instance of InsertSensorRecord by providing instances of PLC, Arduino, and Thera classes. Call the record_time() method to start the data recording process.

    Example:
        plc_instance = PLC()
        arduino_instance = Arduino()
        thera_instance = Thera()
        sensor_recorder = InsertSensorRecord(plc_instance, arduino_instance, thera_instance)
        recorded_data = sensor_recorder.record_time()"""

    def __init__(self, plc, arduino, thera) -> None:
        self.plc = plc
        self.arduino = arduino
        self.sensing_time = 30
        self.thera = thera

    def record_time(self):
        now = datetime.combine(datetime.min, datetime.now().time())
        print(f"Now: {now.time()}, it's sensing time!")

        # Sensing the water condition
        print("Sensor pump has been switched on")
        self.plc.write_plc(id=3, switch=True)
        time.sleep(self.sensing_time / 2)
        # Wait before sensing

        # Get data from arduino
        print("get data sensor")
        recorded_data = list(self.arduino.get_all()["data"].values())
        recorded_data.extend([self.thera.get_data_kwh(), get_data_co2()])
        time.sleep(self.sensing_time / 2)

        self.plc.write_plc(id=3, switch=False)
        print("Sensor pump has been switched off")

        # Save the recorded data to database
        add_sensor_record = SensorRecord(
            id=SensorRecord.objects.count() + 1,
            ec=recorded_data[0],
            ph=recorded_data[1],
            do=recorded_data[2],
            water_temp=recorded_data[3],
            kwh=recorded_data[4],
            co2=recorded_data[5],
        )
        add_sensor_record.save()

        return recorded_data
