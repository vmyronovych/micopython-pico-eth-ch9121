from machine import UART, Pin
from pico_ch9121.config.writer import ConfigWriter
from pico_ch9121.config.reader import ConfigReader
import time

class TcpClientSocket:
    def __init__(self, destinationIp, destinationPortNumber):
        cw = ConfigWriter()
        cw.begin()
        cw.p1_dest_ip(destinationIp)
        cw.p1_dest_port(destinationPortNumber)
        cw.end()

        cr = ConfigReader()
        cr.begin()
        baud_rate = cr.p1_baud_rate()
        dest_ip = cr.p1_dest_ip()
        dest_port = cr.p1_dest_port()
        print(f"soc|new|{dest_ip}:{dest_port}|{baud_rate}")
        cr.end()

        self.__uart = UART(0, baudrate=baud_rate, tx=Pin(0), rx=Pin(1))

        configPin = Pin(14, Pin.OUT,Pin.PULL_UP)
        configPin.value(1)

        print("ch9121|reset|start")
        resetPin = Pin(17, Pin.OUT,Pin.PULL_UP)
        resetPin.value(0)
        time.sleep(.1)
        resetPin.value(1)
        time.sleep(.1)
        print("ch9121|reset|done")

    def send_utf8_str(self, data):
        return self.__uart.write(bytes(data, "UTF-8"))

    # waits synchronously until data recieved or timeout happened
    def receive_sync(self, timeout):
        sleep = 0.001
        waited = 0

        buff = []

        while True:
            while self.__uart.any() > 0:
                buff.append(self.__uart.read(self.__uart.any()))

            if (len(buff) > 0):
                return buff

            time.sleep(sleep)

            if waited > timeout:
                return None

            waited += sleep

# TcpClientSocket usage example
if __name__ == '__main__':

    from pico_ch9121 import config
    from pico_ch9121.config import reader, writer

    cw = writer.ConfigWriter()
    cw.begin()

    cw.dhcp_on()
    cw.gateway_ip("192.168.1.1")
    cw.subnet_mask("255.255.255.0")

    cw.p1_tcp_client()
    cw.p1_device_port(5000)
    cw.p1_baud_rate(9600)
    cw.p1_uart_bits(1, 4, 8)

    cw.end()

    cr = reader.ConfigReader()
    cr.print_net()
    cr.print_p1()

    from pico_ch9121.socket import ClientSocket
    socket = TcpClientSocket("192.168.1.51", 6969)

    while True:
        print(f'sent bytes: {socket.send_utf8_str("Hello")}')
        print(f'resp: {socket.receive_sync(0.01)}')
        time.sleep(5)