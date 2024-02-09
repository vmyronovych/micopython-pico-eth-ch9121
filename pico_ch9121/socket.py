from machine import UART, Pin
from pico_ch9121.config.writer import ConfigWriter
from pico_ch9121.config.reader import ConfigReader
import time

class ClientSocket:
    def __init__(self, destinationIp, destinationPortNumber):
        print("\fNew client socket")
        configWriter = ConfigWriter()
        print("\fNew client socket: begin_config")
        configWriter.begin()
        configWriter.p1_dest_ip(destinationIp)
        configWriter.p1_dest_port(destinationPortNumber)
        configWriter.end()
        
        configReader = ConfigReader()
        configReader.begin()
        uartBaudRate = configReader.p1_baud_rate()        
        print(f'Destination port: {configReader.p1_dest_port()}')
        print(f'Destination IP:   {configReader.p1_dest_ip()}')
        print(f'Baud rate:        {uartBaudRate}')
        print()
        configReader.end()

        self.__uart = UART(0, baudrate=uartBaudRate, tx=Pin(0), rx=Pin(1))
        
        configPin = Pin(14, Pin.OUT,Pin.PULL_UP)
        configPin.value(1)

        print("resetting CH9121")
        resetPin = Pin(17, Pin.OUT,Pin.PULL_UP)
        resetPin.value(0)
        time.sleep(1)
        resetPin.value(1)
        time.sleep(1)
        print("reset is done")

    def send(self, data):
        # send request
        self.__uart.write(data)

        # wait for response synchronously
        waitTimeoutMs = 100
        sleepMs = 1
        sleepSeconds = sleepMs / 1000
        print(sleepSeconds)
        waitedMs = 0
        while True:
            if waitedMs > waitTimeoutMs:
                print("Wait timeout")
                print(waitedMs)
                return None
            time.sleep(sleepSeconds)
            waitedMs += sleepMs
            if self.__uart.any() > 0:
                responseData = self.__uart.read(self.__uart.any())
                print(responseData)
                return responseData

# ClientSocket usage example
if __name__ == '__main__':

    from pico_ch9121 import config
    from pico_ch9121.config import reader, writer
    
    configWriter = writer.ConfigWriter()
    configWriter.begin()

    configWriter.dhcp_on()
    #configWriter.device_ip("192.168.1.30")
    configWriter.gateway_ip("192.168.1.1")
    configWriter.subnet_mask("255.255.255.0")

    configWriter.p1_tcp_client()
    configWriter.p1_device_port(5000)
    configWriter.p1_baud_rate(9600)
    configWriter.p1_uart_bits(1, 4, 8)
    
    configWriter.end()

    configReader = reader.ConfigReader()
    configReader.print()

    from pico_ch9121.socket import ClientSocket
    socket = ClientSocket("192.168.1.51", 6969)

    while True:
        response = socket.send("Hello")
        print(response)
        time.sleep(10)