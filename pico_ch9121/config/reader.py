import time
from machine import UART, Pin
from operations import Op

class ConfigReader:
    def __init__(self):
        uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

    #Chip's IP address
    #Methods:
    #   readIpString
    #Possible values: 4bytes array, e.g.: 0xc0 0xa8 0x01 0xc8
    def DeviceIpAddress(self):
        return self.self.__read(0x61)
    
    def __read(self, command):
        fullCommand = [0x57, 0xab]
        fullCommand.append(command)
        self.uart.write(bytearray(fullCommand))
        while True:
            while self.uart.any() > 0: # check if there is response
                return self.uart.read() # read response
            time.sleep(0.01) # sleep before checking for response again

    
