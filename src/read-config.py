from machine import UART, Pin
import time

READ_DESTINATION_PORT_NUMBER = 0x66
READ_SOURCE_PORT_NUMBER = 0x64

def readInt(uart, command):
    return int.from_bytes(read(uart, command),'little')

def read(uart, command):
    fullCommand = [0x57, 0xab]
    fullCommand.append(command)
    uart.write(bytearray(fullCommand)) # Read the destinationport number of chip port1
    while True:
        while uart.any() > 0: # wait for response
            return uart.read() # read response
        time.sleep(0.01)

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
CFG = Pin(14, Pin.OUT,Pin.PULL_UP)

print("begin")
CFG.value(0)
time.sleep(0.1)

print(readInt(uart0, READ_DESTINATION_PORT_NUMBER))
print(readInt(uart0, READ_SOURCE_PORT_NUMBER))

CFG.value(1)
time.sleep(0.1)
print("end")


