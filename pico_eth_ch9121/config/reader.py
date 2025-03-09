import time
from machine import UART, Pin

class ConfigReader:
    def begin(self):
        self.__config_pin = Pin(14, Pin.OUT,Pin.PULL_UP)
        self.__uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))        
        self.__config_pin.value(0)
        self.__uart.read(self.__uart.any()) # flusing uart buffer before reading settings
        time.sleep(0.01)

    def end(self):
        #self.__leave_port_config_mode()
        self.__config_pin.value(1)
        time.sleep(0.01)

    def device_ip(self):
        return self.__read_ip_str(0x61)

    def subnet_mask(self):
        return self.__read_ip_str(0x62)

    def gateway_ip(self):
        return self.__read_ip_str(0x63)

    def device_mac(self):
        return self.__read_mac_str(0x81)

    # Read network mode for first serial port
    # Possible values:
    #   0x00: TCP server
    #   0x01: TCP client
    #   0x02: UDP server
    #   0x03: UDP client
    def p1_mode(self):
        return self.__read_int(0x60)

    def p1_device_port(self):
        return self.__read_int(0x64)

    def p1_dest_port(self):
        return self.__read_int(0x66)

    def p1_dest_ip(self):
        return self.__read_ip_str(0x65)

    def p1_baud_rate(self):
        return self.__read_int(0x71)

    # Read port 1 serial port check bit data bit stop bit
    # 0x01 0x04 0x08
    # (1stop,noproofreading,8data)
    # Check:: 
    #   0x00: even
    #   0x01: add
    #   0x02: mark
    #   0x03: Space
    #   0x04: None
    def p1_uart_bits(self):
        return self.__read_uart_bits_str(0x72)

    # Serial port's timeout time in milliseconds
    # 0x01 (Serial timeout 1*5ms)
    def p1_timeout(self):
        return self.__read_int(0x73)
    
    # Query port 1 TCP connection status
    # Possible values:
    #   0x00:TCP Disconnect
    #   0x01:TCP Connect
    def p1_tcp_conn_status(self):
        return self.__read_int(0x03)

    def p2_enabled(self):
        return self.__read_int(0x90)

    # Possible values:
    #   0x00: TCP server
    #   0x01: TCP client
    #   0x02: UDP server
    #   0x03: UDP client
    def p2_mode(self):
        return self.__read_int(0x90)

    def p2_device_port(self):
        return self.__read_int(0x91)

    def p2_dest_port(self):
        return self.__read_int(0x93)

    def p2_dest_ip(self):
        return self.__read_ip_str(0x92)

    def p2_baud_rate(self):
        return self.__read_int(0x94)

    # Read port 2 serial port check bit data bit stop bit
    # 0x01 0x04 0x08
    # (1stop,noproofreading,8data)
    # Check::
    #   0x00: even
    #   0x01: add
    #   0x02: mark
    #   0x03: Space
    #   0x04: None
    def p2_uart_bits(self):
        return self.__read_uart_bits_str(0x95)

    # Serial port's timeout time in milliseconds
    # 0x01 (Serial timeout 1*5ms)
    def p2_timeout(self):
        return self.__read_int(0x96)

    def print_net(self):
        self.begin()
        print("\nDevice Network")
        print("==============")
        print(f'IP:                      {self.device_ip()}')
        print(f'Gateway:                 {self.gateway_ip()}')
        print(f'Subnet:                  {self.subnet_mask()}')
        print(f'MAC:                     {self.device_mac()}')
        self.end()

    def print_p1(self):
        self.begin()
        print("\nUART 1")
        print("======")
        print(f'Network mode:             {self.p1_mode()}')
        print(f'Device port:              {self.p1_device_port()}')
        print(f'Destination port:         {self.p1_dest_port()}')
        print(f'Destination IP:           {self.p1_dest_ip()}')
        print(f'Baud rate:                {self.p1_baud_rate()}')
        print(f'Bits (stop, check, data): {self.p1_uart_bits()}')
        print(f'Timeout:                  {self.p1_timeout()}ms')
        self.end()

    def print_p2(self):
        self.begin()
        print("\nUART 2")
        print("======")
        print(f'Network mode:             {self.p2_mode()}')
        print(f'Device port:              {self.p2_device_port()}')
        print(f'Destination port:         {self.p2_dest_port()}')
        print(f'Destination IP:           {self.p2_dest_ip()}')
        print(f'Baud rate:                {self.p2_baud_rate()}')
        print(f'Bits (stop, check, data): {self.p2_uart_bits()}')
        print(f'Timeout:                  {self.p2_timeout()}ms')
        self.end()

    # Leave serial port configuration mode (Only on the serial port negotiating side Formula is valid)
    def __leave_port_config_mode(self):
        self.__uart.write(bytearray([0x57, 0xab, 0x5e]))

    def __read_ip_str(self, cmd):
        ip = self.__read(cmd)
        return "{}.{}.{}.{}".format(ip[0], ip[1], ip[2], ip[3])

    def __read_int(self, cmd):
        return int.from_bytes(self.__read(cmd),'little')

    def __read_mac_str(self, cmd):
        mac = self.__read(cmd)
        return "{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}".format(
            mac[0], mac[1], mac[2], mac[3], mac[4], mac[5])

    def __read_uart_bits_str(self, cmd):
        uart_bits = self.__read(cmd)
        return "{},{},{}".format(uart_bits[0], uart_bits[1], uart_bits[2])

    def __read(self, cmd):
        self.__uart.read(self.__uart.any()) # flusing uart buffer before reading settings
        full_cmd = [0x57, 0xab]
        full_cmd.append(cmd)
        time.sleep(.001)
        self.__uart.write(bytearray(full_cmd))
        time.sleep(.001)
        while True:
            while self.__uart.any() > 0: # check if there is response
                return self.__uart.read() # read response
            time.sleep(.001) # sleep before checking for response again


# Print configuration when this module is run as standalone python script
if __name__ == '__main__':
    cr = ConfigReader()
    cr.print_net()
    cr.print_p1()
    cr.print_p2()
