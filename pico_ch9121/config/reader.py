import time
from machine import UART, Pin

class ConfigReader:
    def begin(self):
        self.__configPin = Pin(14, Pin.OUT,Pin.PULL_UP)
        self.__uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))        
        self.__configPin.value(0)
        self.__uart.read(self.__uart.any()) # flusing uart buffer before reading settings
        time.sleep(0.01)
    
    def end(self):        
        #self.__leave_port_config_mode()
        self.__configPin.value(1)
        time.sleep(0.01)

    def device_ip(self):
        return self.__readIpString(0x61)
    
    def subnet_mask(self):
        return self.__readIpString(0x62)

    def gateway_ip(self):
        return self.__readIpString(0x63)
    
    def device_mac(self):
        return self.__readMacAddressString(0x81)

    
    # Read network mode for first serial port
    # Possible values: 
    #   0x00: TCP server
    #   0x01: TCP client
    #   0x02: UDP server
    #   0x03: UDP client
    def p1_mode(self):
        return self.__readInt(0x60)
    
    def p1_device_port(self):
        return self.__readInt(0x64)
    
    def p1_dest_port(self):
        return self.__readInt(0x66)
    
    def p1_dest_ip(self):
        return self.__readIpString(0x65)
    
    def p1_baud_rate(self):
        return self.__readInt(0x71)
    
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
        return self.__readUartBitsString(0x72)
    
    # Serial port's timeout time in milliseconds
    # 0x01 (Serial timeout 1*5ms)
    def p1_timeout(self):
        return self.__readInt(0x73)
    
    def p2_enabled(self):
        return self.__readInt(0x90)

    # Possible values: 
    #   0x00: TCP server
    #   0x01: TCP client
    #   0x02: UDP server
    #   0x03: UDP client
    def p2_mode(self):
        return self.__readInt(0x90)
    
    def p2_device_port(self):
        return self.__readInt(0x91)
    
    def p2_dest_port(self):
        return self.__readInt(0x93)
    
    def p2_dest_ip(self):
        return self.__readIpString(0x92)
    
    def p2_baud_rate(self):
        return self.__readInt(0x94)
    
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
        return self.__readUartBitsString(0x95)
    
    # Serial port's timeout time in milliseconds
    # 0x01 (Serial timeout 1*5ms)
    def p2_timeout(self):
        return self.__readInt(0x96)
    
    def print(self):
        self.begin()

        print("\nDevice Network")
        print("==============")
        
        print(f'IP:                      {self.device_ip()}')
        print(f'Gateway:                 {self.gateway_ip()}')
        print(f'Subnet:                  {self.subnet_mask()}')
        print(f'MAC:                     {self.device_mac()}')

        print("\nUART 1")
        print("======")

        print(f'Network mode:             {self.p1_mode()}')
        print(f'Device port:              {self.p1_device_port()}')
        print(f'Destination port:         {self.p1_dest_port()}')
        print(f'Destination IP:           {self.p1_dest_ip()}')
        print(f'Baud rate:                {self.p1_baud_rate()}')
        print(f'Bits (stop, check, data): {self.p1_uart_bits()}')
        print(f'Timeout:                  {self.p1_timeout()}ms')
        
        # print("\nUART 2")
        # print("======")

        # print(f'Network mode:             {self.p2_network_mode()}')
        # print(f'Device port:              {self.p2_device_port_number()}')
        # print(f'Destination port:         {self.p2_destination_port_number()}')
        # print(f'Destination IP:           {self.p2_destination_ip()}')
        # print(f'Baud rate:                {self.p2_uart_baud_rate()}')
        # print(f'Bits (stop, check, data): {self.p2_uart_bits()}')
        # print(f'Timeout:                  {self.p2_timeout()}ms')

        self.end()
    
    # Leave serial port configuration mode (Only on the serial port negotiating side Formula is valid)
    def __leave_port_config_mode(self):
        self.__uart.write(bytearray([0x57, 0xab, 0x5e]))

    def __readIpString(self, command):
        ipBytes = self.__read(command)
        return "{}.{}.{}.{}".format(ipBytes[0], ipBytes[1], ipBytes[2], ipBytes[3])
    
    def __readInt(self, command):
        return int.from_bytes(self.__read(command),'little')

    def __readMacAddressString(self, command):
        ipBytes = self.__read(command)
        return "{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}".format(
            ipBytes[0], ipBytes[1], ipBytes[2], ipBytes[3], ipBytes[4], ipBytes[5])

    def __readUartBitsString(self, command):
        ipBytes = self.__read(command)
        return "{},{},{}".format(ipBytes[0], ipBytes[1], ipBytes[2])
    
    def __read(self, command):
        self.__uart.read(self.__uart.any()) # flusing uart buffer before reading settings
        fullCommand = [0x57, 0xab]
        fullCommand.append(command)
        self.__uart.write(bytearray(fullCommand))
        while True:
            while self.__uart.any() > 0: # check if there is response
                return self.__uart.read() # read response
            time.sleep(0.01) # sleep before checking for response again


# Print configuration when this module is run as standalone python script
if __name__ == '__main__':
    config = ConfigReader()
    config.print()
