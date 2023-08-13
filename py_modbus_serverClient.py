'''
Pymodbus Server With Updating Thread
--------------------------------------------------------------------------
This is an example of having a background thread updating the
context while the server is operating. This can also be done with
a python thread::
    from threading import Thread
    thread = Thread(target=updating_writer, args=(context,))
    thread.start()
'''
#---------------------------------------------------------------------------# 
# import the modbus libraries we need
#---------------------------------------------------------------------------# 
from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer

#---------------------------------------------------------------------------# 
# import the twisted libraries we need
#---------------------------------------------------------------------------# 
from twisted.internet.task import LoopingCall

#---------------------------------------------------------------------------# 
# configure the service logging
#---------------------------------------------------------------------------# 
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

#---------------------------------------------------------------------------# 
# for database reading
#---------------------------------------------------------------------------# 

import sqlite3
import sys

sqlite_file = 'ModbusTable.db'

thermostats = 25
registers_per_thermostat = 3

global total_registers
total_registers = thermostats * registers_per_thermostat

#---------------------------------------------------------------------------# 
# define your callback process
#---------------------------------------------------------------------------# 
def updating_writer(a):
    ''' A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.
    :param arguments: The input arguments to the call
    '''
    # log.debug("updating the context")
    context  = a[0]
    functioncode = 3 
    slave_id = 0x01 # slave address
    address  = 0x10 # start register : 400017

    values = [0]

    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c1 = conn.cursor()

    c1.execute("""SELECT ID, SetPoint, ActualTemp FROM ModbusData""")

    registers = c1.fetchall()

    c1.close()

    for register in registers:
        for value in register:
            values.append(value)

    # log.debug("values from database: " + str(values))

    context[slave_id].setValues(functioncode, address, values)

    values = context[slave_id].getValues(functioncode, address, count=total_registers)

    # log.debug("values to be written to database: " + str(values))

    c2 = conn.cursor()

    for index in range(len(values)):
        if (index+2)<len(values):
            column1 = values[index]
            column2 = values[index+1]
            column3 = values[index+2]
            c2.execute("""UPDATE ModbusData set SetPoint = ?, ActualTemp = ? where ID=?""",[column2, column3, column1])

    # Committing changes and closing the connection to the database file
    c2.close()
    conn.close()



#---------------------------------------------------------------------------# 
# initialize your data store
#---------------------------------------------------------------------------# 
store = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0, [0]*total_registers),
    co = ModbusSequentialDataBlock(0, [0]*total_registers),
    hr = ModbusSequentialDataBlock(0, [0]*total_registers),
    ir = ModbusSequentialDataBlock(0, [0]*total_registers))
context = ModbusServerContext(slaves=store, single=True)

#---------------------------------------------------------------------------# 
# initialize the server information
#---------------------------------------------------------------------------# 
identity = ModbusDeviceIdentification()
identity.VendorName  = 'pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl   = 'http://github.com/bashwork/pymodbus/'
identity.ProductName = 'pymodbus Server'
identity.ModelName   = 'pymodbus Server'
identity.MajorMinorRevision = '1.0'

#---------------------------------------------------------------------------# 
# run the server you want
#---------------------------------------------------------------------------# 
time = 5 # 5 seconds delay
loop = LoopingCall(f=updating_writer, a=(context,))
loop.start(time, now=False) # initially delay by time
# updating_writer(10)
StartTcpServer(context, identity=identity, address=("192.168.250.100", 1024))
# StartTcpServer(context, identity=identity, address=('localhost', 1024))