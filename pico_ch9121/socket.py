from machine import UART, Pin
from pico_ch9121.config.writer import ConfigWriter
from pico_ch9121.config.reader import ConfigReader
import time

class ClientSocket:
    def __init__(self, destinationIp, destinationPortNumber):
        configWriter = ConfigWriter()
        configWriter.begin_config()
        configWriter.port1_destination_ip(destinationIp)
        configWriter.port1_destination_port_number(destinationPortNumber)
        configWriter.end_config()
        
        configReader = ConfigReader()
        configReader.begin_read()
        uartBaudRate = configReader.port1_uart_baud_rate()
        configReader.end_read()

        self.__uart = UART(0, baudrate=uartBaudRate, tx=Pin(0), rx=Pin(1))

    def send(self, data):
        # send request
        self.__uart.write(data)

        # wait for response synchronously
        waitTimeoutMs = 50
        sleepMs = 1
        sleepSeconds = sleepMs / 1000
        waitedMs = 0
        while True:
            if waitedMs > waitTimeoutMs:
                print("Wait timeout")
                return None
            time.sleep(sleepSeconds)
            waitedMs += sleepMs
            if self.__uart.any() > 0:
                responseData = self.__uart.read(self.__uart.any())
                print(responseData)
                return responseData

# Print configuration when this module is run as standalone python script
if __name__ == '__main__':
    from pico_ch9121.socket import ClientSocket
    socket = ClientSocket("192.168.1.40", 6969)
    response = socket.send("Hello")
    print(response)

# uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
# CFG = Pin(14, Pin.OUT,Pin.PULL_UP)
# RST = Pin(17, Pin.OUT,Pin.PULL_UP)
# CFG.value(1)
# RST.value(1)

# while True:
#     uart0.write("hello from pico")
#     while uart0.any() > 0:
#         rxData0 = uart0.read()
#         uart0.write(rxData0)
#         print(rxData0)
#     time.sleep(10)
