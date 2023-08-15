import minimalmodbus
import serial
import serial.tools.list_ports as list_ports


class Thera:
    """
    Thera Class
    -----------

    This class provides an interface for communication with a Thera energy meter using the Modbus RTU protocol. It enables reading energy consumption data from the Thera energy meter.

    Attributes:
        slave_address (int): The Modbus slave address of the Thera energy meter.

    Methods:
        __init__(): Initializes the Thera class by establishing a connection to the Thera energy meter using minimalmodbus and a serial connection.
        find_serial_port(): Searches for available serial ports and identifies the one associated with the Thera energy meter.
        get_data_kwh(): Reads and returns the energy consumption data (in kilowatt-hours) from the Thera energy meter.

    Usage:
        Create an instance of the Thera class, optionally specifying the slave address. The class will automatically attempt to connect to the Thera energy meter using the identified serial port. Use the get_data_kwh() method to retrieve energy consumption data.

    Example:
        thera_instance = Thera(slave_address=1)
        energy_consumption = thera_instance.get_data_kwh()
        print("Energy Consumption (kWh):", energy_consumption)"""

    def __init__(self, slave_address=8) -> None:
        self.slave_address = slave_address
        try:
            self.serial_port_thera = self.find_serial_port()
            self.thera_instrument = minimalmodbus.Instrument(
                port=self.serial_port_thera, slaveaddress=self.slave_address
            )
            self.serial_port = serial.Serial(
                self.serial_port_thera,
                baudrate=9600,
                bytesize=8,
                parity=serial.PARITY_NONE,
                stopbits=1,
                timeout=2,
            )

            # Attach the serial port instance to the minimalmodbus instrument
            self.thera_instrument.serial = self.serial_port
            self.thera_instrument.mode = minimalmodbus.MODE_RTU
            self.thera_instrument.clear_buffers_before_each_transaction = True

        except:
            print("Device not found!")

    def find_serial_port(self):
        ports = list_ports.comports()
        for port in ports:
            if "FT232R" in port.description.split(" "):
                return port.device
        return ""

    def get_data_kwh(self):
        return self.thera_instrument.read_register(13, functioncode=3) * 0.1
