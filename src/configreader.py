import time

#Working mode of chip port 1
#Methods:
#   readInt
#Possible values: 
#   0x00: TCP server
#   0x01: TCP client
#   0x02: UDP server
#   0x03: UDP client
READ_PORT_1_NETWORK_MODE = 0x60

#Chip's IP address
#Methods:
#   readIpString
#Possible values: 4bytes array, e.g.: 0xc0 0xa8 0x01 0xc8
READ_DEVICE_IP_ADDRESS = 0x61

#Chip's subnet mask
#Methods:
#   readIpString
#Possible values: 4bytes array, e.g.: 0xff 0xff 0xff 0x00
READ_DEVICE_SUBNET_MASK = 0x62

#Chip's gateway address
#Methods:
#   readIpString
#Possible values: 4bytes array, e.g.: 0xc0 0xa8 0x01 0xc01
READ_GATEWAY_IP_ADDRESS = 0x63

#Port number of chip's port 1
#Methods:
#   readInt
#Possible values: bytes array representing int port number, e.g. 0xd0 0x07
READ_DEVICE_PORT_1_NUMBER = 0x64

#Destination IP address of chip's port 1 (address of server where the chip wants to send requests to)
#Methods:
#   readIpString
#Possible values: 4bytes array, e.g.: 0xc0 0xa8 0x01 0xc8
READ_DESTINATION_IP_1_ADDRESS = 0x65

#The destination port number of chip's port 1
#Methods:
#   readInt
#Possible values: bytes array representing int port number, e.g. 0xd0 0x07
READ_DESTINATION_PORT_1_NUMBER = 0x66

#Baud rate of chip's serial port 1
#Methods:
#   readInt
#Possible values: bytes array representing baud rate as int, e.g. 0x80 0x25 0x00 0x00
READ_SERIAL_PORT_1_BAUD_RATE = 0x71

#Stop bit, check bit, data bits amount for chip's serial port 1
#Methods:
#   readUartBitsString
#Possible values: 
#   0x00: even
#   0x01: add
#   0x02: mark
#   0x03: Space
#   0x04: None
READ_SERIAL_PORT_1_STOP_CHECK_DATA_BITS = 0x72

#Serial port's timeout time (in ms) for chip's serial port 1
#Methods:
#   readInt
#Possible values: integer
READ_SERIAL_PORT_1_TIMEOUT_TIME = 0x73

#Chip's MAC address
#Methods:
#   readMacAddressString
#Possible values: mac address in format XX:XX:XX:XX:XX:XX
READ_DEVICE_MAC_ADDRESS = 0x81

#Working mode of chip port 2
#Methods:
#   readInt
#Possible values: 
#   0x00: TCP server
#   0x01: TCP client
#   0x02: UDP server
#   0x03: UDP client
READ_PORT_2_NETWORK_MODE = 0x90

#Port number of chip's port 2
#Methods:
#   readInt
#Possible values: bytes array representing int port number, e.g. 0xd0 0x07
READ_DEVICE_PORT_2_NUMBER = 0x91

#Destination IP address of chip's port 2 (address of server where the chip wants to send requests to)
#Methods:
#   readIpString
#Possible values: 4bytes array, e.g.: 0xc0 0xa8 0x01 0xc8
READ_DESTINATION_IP_2_ADDRESS = 0x92

#The destination port number of chip's port 2
#Methods:
#   readInt
#Possible values: bytes array representing int port number, e.g. 0xd0 0x07
READ_DESTINATION_PORT_2_NUMBER = 0x93

#Baud rate of chip's serial port 2
#Methods:
#   readInt
#Possible values: bytes array representing baud rate as int, e.g. 0x80 0x25 0x00 0x00
READ_SERIAL_PORT_2_BAUD_RATE = 0x94

#Stop bit, check bit, data bits amount for chip's serial port 2
#Methods:
#   readUartBitsString
#Possible values: 
#   0x00: even
#   0x01: add
#   0x02: mark
#   0x03: Space
#   0x04: None
READ_SERIAL_PORT_2_STOP_CHECK_DATA_BITS = 0x95

def readInt(uart, command):
    return int.from_bytes(read(uart, command),'little')

def readMacAddressString(uart, command):
    ipBytes = read(uart, command)
    return "{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}".format(
        ipBytes[0], ipBytes[1], ipBytes[2], ipBytes[3], ipBytes[4], ipBytes[5])


def readIpString(uart, command):
    ipBytes = read(uart, command)
    return "{}.{}.{}.{}".format(ipBytes[0], ipBytes[1], ipBytes[2], ipBytes[3])

def readUartBitsString(uart, command):
    ipBytes = read(uart, command)
    return "{},{},{}".format(ipBytes[0], ipBytes[1], ipBytes[2])

def read(uart, command):
    fullCommand = [0x57, 0xab]
    fullCommand.append(command)
    uart.write(bytearray(fullCommand)) # Read the destinationport number of chip port1
    while True:
        while uart.any() > 0: # wait for response
            return uart.read() # read response
        time.sleep(0.01)

def printAll(uart):
    print(readInt(uart, READ_PORT_1_NETWORK_MODE))

    print(readInt(uart, READ_DESTINATION_PORT_1_NUMBER))
    print(readInt(uart, READ_DEVICE_PORT_1_NUMBER))

    print(readIpString(uart, READ_DEVICE_IP_ADDRESS))
    print(readIpString(uart, READ_DEVICE_SUBNET_MASK))
    print(readIpString(uart, READ_GATEWAY_IP_ADDRESS))
    print(readIpString(uart, READ_DESTINATION_IP_1_ADDRESS))
    print(readInt(uart, READ_SERIAL_PORT_1_BAUD_RATE))
    print(readUartBitsString(uart, READ_SERIAL_PORT_1_STOP_CHECK_DATA_BITS))
    print(readInt(uart, READ_SERIAL_PORT_1_TIMEOUT_TIME))

    print(readMacAddressString(uart, READ_DEVICE_MAC_ADDRESS))

    print(readInt(uart, READ_PORT_2_NETWORK_MODE))
    print(readInt(uart, READ_DEVICE_PORT_2_NUMBER))
    print(readIpString(uart, READ_DESTINATION_IP_2_ADDRESS))
    print(readInt(uart, READ_DESTINATION_PORT_2_NUMBER))
    print(readInt(uart, READ_SERIAL_PORT_2_BAUD_RATE))
    print(readUartBitsString(uart, READ_SERIAL_PORT_2_STOP_CHECK_DATA_BITS))