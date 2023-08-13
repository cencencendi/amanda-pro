import serial.tools.list_ports
import json


class Arduino:
    """
    Arduino Class
    -------------

    This class provides an interface for communicating with an Arduino device. It allows you to send commands and retrieve data from the Arduino using a serial connection.

    Attributes:
        serial_port_arduino (str): The serial port to which the Arduino is connected.
        arduino (serial.Serial): A serial connection object used to communicate with the Arduino.

    Methods:
        __init__(): Initializes the Arduino class by attempting to establish a serial connection with the Arduino.
        find_serial_port(): Searches for available serial ports and identifies the one associated with the Arduino.
        get_all(): Sends a command to the Arduino to retrieve sensor data and returns the collected data in JSON format.

    Usage:
        Create an instance of the Arduino class. The class will automatically attempt to connect to the Arduino using the identified serial port. Call the get_all() method to request and retrieve sensor data from the Arduino.

    Example:
        arduino_instance = Arduino()
        sensor_data = arduino_instance.get_all()
        print("Retrieved Sensor Data:", sensor_data)"""

    def __init__(self) -> None:
        try:
            self.serial_port_arduino = self.find_serial_port()
            self.arduino = serial.Serial(port=self.serial_port_arduino, baudrate=9600, timeout=3)
        except Exception as e:
            print(e)

    def find_serial_port(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB" in port.description.split(" "):
                return port.device
        return None

    def get_all(self):
        command = json.dumps({"cmd": "get_all"})
        print("Command sent to Arduino")

        self.arduino.write(command.encode() + b"\n\r")
        try:
            data = self.arduino.readline().decode("ascii")
            return json.loads(data)
        except Exception as e:
            print(f"There was an error: {e}")
            dummy_data = '{"data":{"RTD":"0","pH":"0","EC":"0","DO":"0"}}'
            return json.loads(dummy_data)