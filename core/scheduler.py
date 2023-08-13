from apscheduler.schedulers.background import BackgroundScheduler
from .dosing_cycle import DosingCycle
from .growlights_control import GrowlightsControl
from .insert_sensor_record import InsertSensorRecord
from .arduino import Arduino
from .plc import PLC
from .thera import Thera
from .watering_irrigation import Watering
import threading

arduino_mega = Arduino()
thera_instrument = Thera()
omron_plc = PLC()

insert_sensor_record = InsertSensorRecord(
    plc=omron_plc, arduino=arduino_mega, thera=thera_instrument
)
dosing_cycle = DosingCycle(insert_sensor_record=insert_sensor_record)
growlights_control = GrowlightsControl(plc=omron_plc)
watering_plant = Watering(plc=omron_plc)

scheduler = BackgroundScheduler()


def start(register):
    if register:
        return

    print(">> Scheduler started!")

    watering_thread = threading.Thread(target=lambda: watering_plant.check_time(dosing_cycle))
    scheduler.add_job(
        func=dosing_cycle.dosing_control, trigger="interval", minutes=5, name="dosing control"
    )
    scheduler.add_job(
        func=growlights_control.control, trigger="interval", seconds=1, name="growlights control"
    )
    watering_thread.start()
    scheduler.start()


def stop():
    print("stopped")
    scheduler.shutdown()