from pyModbusTCP.client import ModbusClient


devices = [
    0,  # 0 system
    0,  # 1 toggle utama
    0,  # 2 pompa plant
    0,  # 3 pompa sensor
    0,  # 4 peristaltic 1 (Nutrisi A& B)
    0,  # 5 peristaltic 2 (pH)
    0,  # 6 valve CO2
    0,  # 7 valve water tank
    0,  # 8 stirrer (A&B)
    0,  # 9 stirrer pH
    0,  # 10 volume A&B
    0,  # 11 volume pH
    0,  # 12 toggle mist sprayer
    0,  # 13 toggle peristaltic 1
    0,  # 14 toggle peristaltic 2
    0,  # 15 toggle growlight 1
    0,  # 16 toggle growlight 2
    0,  # 17 toggle growlight 3
    0,  # 18 toggle growlight 4
    0,  # 19 toggle growlight 5
    0,  # 20 toggle valve flush
    0,  # 21 Cap Sensor Low
    0,  # 22 Cap Sensor Med
    0,  # 23 Cap Sensor High
    0,  # 24 Flow Meter Intake
    0,  # Kosong
    0,  # 26 Flow Meter Plant
    0,
]


class PLC:
    """
    PLC Class
    ---------

    This class provides an interface for communication with a PLC (Programmable Logic Controller) using the Modbus TCP protocol. It allows reading and writing data to specific registers on the PLC.

    Attributes:
        host (str): The IP address or hostname of the target PLC.
        port (int): The port number to use for the Modbus TCP communication.
        devices (list): A list of values representing the state of various devices and registers on the PLC.

    Methods:
        __init__(): Initializes the PLC class by establishing a connection to the target PLC using ModbusClient.
        write_plc(id, switch, mililiter=0): Writes the state of a specified device or register to the PLC. Also, optionally sets the mililiter value for specific devices.
        read_capacitor(register): Reads the value of a specified register on the PLC representing a capacitor.

    Usage:
        Create an instance of the PLC class, specifying the target PLC's host and port. Use the write_plc() method to toggle devices or registers and set mililiter values where needed. Use the read_capacitor() method to read the value of a capacitor-related register.

    Example:
        plc_instance = PLC(host="192.168.250.100", port=1024)
        plc_instance.write_plc(id=3, switch=True)  # Turn on sensor pump
        capacitor_value = plc_instance.read_capacitor(register=21)  # Read value from Cap Sensor Low register
        print("Capacitor Value:", capacitor_value)"""

    def __init__(self, host="192.168.250.100", port=1024, devices=devices) -> None:
        self.host = host
        self.port = port
        self.devices = devices
        try:
            self.plc = ModbusClient(
                self.host, self.port, auto_open=True, auto_close=True, timeout=10
            )

        except Exception as e:
            print(e)

    def write_plc(self, id, switch, mililiter=0):
        self.devices[id] = switch
        if id == 4:
            self.devices[10] = mililiter
        if id == 5:
            self.devices[11] = mililiter

        try:
            if not self.plc.is_open and not self.plc.open():
                return print("Unable to connect to PLC")

            if not self.plc.write_multiple_registers(16, self.devices):
                return print(f"Error writing register {id}")

        except Exception as e:
            print(e)

    def read_capacitor(self, register):
        try:
            if not self.plc.is_open and not self.plc.open():
                return print("Unable to connect to PLC")

            read_holding_register = self.plc.read_holding_registers(register, 1)

            if read_holding_register:
                return read_holding_register[0]
            else:
                print(f"Error read register {register}")

        except Exception as e:
            print(e)
