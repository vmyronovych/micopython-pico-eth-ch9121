from machine import UART, Pin
import time
import configreader

#Working mode of chip port 1
#Methods:
#   writeOneByteInt
#Possible values: 
#   0x00: TCP server
#   0x01: TCP client
#   0x02: UDP server
#   0x03: UDP client
WRITE_PORT_1_NETWORK_MODE = 0x10
NETWORK_MODE_TCP_SERVER = 0
NETWORK_MODE_TCP_CLIENT = 0x1
NETWORK_MODE_UDP_SERVER = 2 
NETWORK_MODE_UDP_CLIENT = 3

#Set port number of chip's port 1
#Methods:
#   writeTwoBytesInt
#Possible values: bytes array representing int port number, e.g. 0xd0 0x07
WRITE_DEVICE_PORT_1_NUMBER = 0x14

#Set destination port number of chip's port 1
#Methods:
#   writeTwoBytesInt
#Possible values: bytes array representing int port number, e.g. 0xd0 0x07
WRITE_DESTINATION_PORT_1_NUMBER = 0x16

def writeOneByteInt(uart, command, value):
    write(uart, command, value.to_bytes(1, 'little'))

def writeTwoBytesInt(uart, command, value):
    write(uart, command, value.to_bytes(2, 'little'))

def write(uart, command, value):
    fullCommand = [0x57, 0xab]
    fullCommand.append(command)

    for v in value:
        fullCommand.append(v)

    fullCommandBytes = bytearray(fullCommand)
    uart.write(fullCommandBytes)
    time.sleep(0.01)

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

CFG = Pin(14, Pin.OUT,Pin.PULL_UP)
RST = Pin(17, Pin.OUT,Pin.PULL_UP)
RST.value(1)

print("begin config writing\n")

CFG.value(0)
time.sleep(0.1)

writeOneByteInt(uart0, WRITE_PORT_1_NETWORK_MODE, NETWORK_MODE_TCP_CLIENT)
writeTwoBytesInt(uart0, WRITE_DEVICE_PORT_1_NUMBER, 5000)
writeTwoBytesInt(uart0, WRITE_DESTINATION_PORT_1_NUMBER, 6969)

time.sleep(0.1)
CFG.value(1)

print("end config writing \n")

print("begin printing configuration...\n")

time.sleep(0.1)

CFG.value(0)

configreader.printAll(uart0)

print("end printing configuration...\n")
