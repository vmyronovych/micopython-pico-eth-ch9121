import time
from machine import UART, Pin

OFF = 0x1

class ConfigWriter:
    def begin(self):
        self.__configPin = Pin(14, Pin.OUT,Pin.PULL_UP)
        self.__uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))        
        time.sleep(0.1)
        self.__configPin.value(0)
        time.sleep(0.1)
        self.__uart.read(self.__uart.any()) # cleanup old data on a line

    def end(self):
        self.__save_to_eeprom()
        self.__execute_config_and_reset()
        self.__leave_port_config_mode()
        self.__configPin.value(1)
        time.sleep(0.1)

    def dhcp_on(self):
        self.dhcp_switch(0x01)

    def dhcp_off(self):
        self.dhcp_switch(0x00)
    
    # Turn DHCP on/off
    # 0x00 - off
    # 0x01 - on
    def dhcp_switch(self, val):
        self.__write(0x33, [val])

    def device_ip(self, ip):
        return self.__writeIp(0x11, ip)
    
    def subnet_mask(self, ipMask):
        return self.__writeIp(0x12, ipMask)

    def gateway_ip(self, ip):
        return self.__writeIp(0x13, ip)
    
    # Set network mode to TCP Server for serial port 1
    def p1_tcp_server(self):
        return self.p1_mode(0x00)
    
    # Set network mode to TCP Client for serial port 1
    def p1_tcp_client(self):
        return self.p1_mode(0x01)
    
    # Set network mode to UDP Server for serial port 1
    def p1_udp_server(self):
        return self.p1_mode(0x02)
    
    # Set network mode to UDP Client for serial port 1
    def p1_udp_client(self):
        return self.p1_mode(0x03)
    
    # Possible values: 
    #   0x00: TCP server
    #   0x01: TCP client
    #   0x02: UDP server
    #   0x03: UDP client
    def p1_mode(self, mode):
        return self.__writeOneByteInt(0x10, mode)
    
    def p1_device_port(self, portNumber):
        return self.__writeTwoBytesInt(0x14, portNumber)
    
    def p1_dest_port(self, portNumber):
        return self.__writeTwoBytesInt(0x16, portNumber)
    
    def p1_dest_ip(self, ip):
        return self.__writeIp(0x15, ip)
    
    # Set Baud Rate for serial port 1
    # for chip configuration mode the rate is always 9600
    # once chip exits configuration mode the baud rate will match the one set by this method
    def p1_baud_rate(self, baudRate):
        return self.__writeFourBytesInt(0x21, baudRate)
    
    # Configure serial 1: calibration bit, data bit, stop bit
    # 0x01 0x04 0x08
    # (1stop,noproofreading,8data)
    # Check:: 
    #   0x00: even
    #   0x01: add
    #   0x02: mark
    #   0x03: Space
    #   0x04: None
    def p1_uart_bits(self, stop, pairty, data):
        return self.__write(0x22, [stop, pairty, data])
    
    # Set timeout for serial port 1 in milliseconds
    # 0x01 (Serial timeout 1*5ms)
    def p1_timeout(self, timeoutMs):
        return self.__writeFourBytesInt(0x23, timeoutMs)
    
    # Turn on port 2
    def p2_on(self):
        return self.p2_toggle(0x01)
    
    # Turn off port 2
    def p2_off(self):
        return self.p2_toggle(0x00)
    
    # Turn port 2 on/off
    # 0x00 - off
    # 0x01 - on
    def p2_toggle(self, val):
        return self.__writeOneByteInt(0x39, val)
    
    # Set network mode to TCP Server for serial port 2
    def p2_tcp_server(self):
        return self.p2_mode(0x00)
    
    # Set network mode to TCP Client for serial port 2
    def p2_tcp_client(self):
        return self.p2_mode(0x01)
    
    # Set network mode to UDP Server for serial port 2
    def p2_udp_server(self):
        return self.p2_mode(0x02)
    
    # Set network mode to UDP Client for serial port 2
    def p2_udp_client(self):
        return self.p2_mode(0x03)

    # Possible values: 
    #   0x00: TCP server
    #   0x01: TCP client
    #   0x02: UDP server
    #   0x03: UDP client
    def p2_mode(self, mode):
        return self.__writeOneByteInt(0x40, mode)
    
    def p2_device_port(self, portNumber):
        return self.__writeTwoBytesInt(0x41, portNumber)
    
    def p2_dest_port(self, portNumber):
        return self.__writeTwoBytesInt(0x43, portNumber)
    
    def p2_dest_ip(self, ip):
        return self.__writeIp(0x42, ip)
    
    # Set Baud Rate for serial port 2
    def p2_baud_rate(self, baudRate):
        return self.__writeFourBytesInt(0x44, baudRate)
    
    # Configure serial port 12 calibration bit, data bit, stop bit
    # 0x01 0x04 0x08
    # (1stop,noproofreading,8data)
    # Check:: 
    #   0x00: even
    #   0x01: add
    #   0x02: mark
    #   0x03: Space
    #   0x04: None
    def p2_uart_bits(self, stop, pairty, data):
        return self.__write(0x45, [stop, pairty, data])
    
    # Set timeout for serial port 2 in milliseconds
    # 0x01 (Serial timeout 1*5ms)
    def p2_timeout(self, timeoutMs):
        return self.__writeFourBytesInt(0x46, timeoutMs)
    
    # Save parameters to EEPROM
    def __save_to_eeprom(self):
        self.__write(0x0d)
    
    # Execute the configuration command, and Reset CH9121
    def __execute_config_and_reset(self):
        self.__write(0x0e)
    
    # Leave serial port configuration mode (Only on the serial port negotiating side Formula is valid)
    def __leave_port_config_mode(self):
        self.__write(0x5e)

    def __writeOneByteInt(self, command, value):
        self.__write(command, value.to_bytes(1, 'little'))

    def __writeTwoBytesInt(self, command, value):
        self.__write(command, value.to_bytes(2, 'little'))
    
    def __writeFourBytesInt(self, command, value):
        self.__write(command, value.to_bytes(4, 'little'))

    def __writeIp(self, command, value):
        ipSegmentsBytes = []
        for ipSegment in value.split("."):
            ipSegmentsBytes.append(int(ipSegment).to_bytes(1, 'little')[0])
        self.__write(command, ipSegmentsBytes)

    def __write(self, command, value = None):
        fullCommand = [0x57, 0xab]
        fullCommand.append(command)
        print(command) # this somehow makes config write work consistant
        if (value != None):
            for v in value:
                fullCommand.append(v)

        fullCommandBytes = bytearray(fullCommand)
        self.__uart.write(fullCommandBytes)
        time.sleep(0.01)

# Write, read and print configuration when this module is run as standalone python script
if __name__ == '__main__':
    from pico_ch9121.config import reader, writer
    # configReader = reader.ConfigReader()
    # configReader.print()

    configWriter = writer.ConfigWriter()
    configWriter.begin()

    configWriter.device_ip("192.168.0.27")
    configWriter.gateway_ip("192.168.0.1")
    configWriter.subnet_mask("255.255.0.127")

    configWriter.p1_tcp_client()
    configWriter.p1_device_port(5001)
    configWriter.p1_dest_port(6970)
    configWriter.p1_dest_ip("192.168.0.158")
    configWriter.p1_baud_rate(9600)
    configWriter.p1_uart_bits(1, 4, 8)
    configWriter.p1_timeout(5)

    configWriter.p2_on()
    configWriter.p2_tcp_server()
    configWriter.p2_device_port(5001)
    configWriter.p2_dest_port(6971)
    configWriter.p2_dest_ip("192.168.1.76")
    configWriter.p2_baud_rate(9600)
    configWriter.p2_uart_bits(1, 4, 8)
    configWriter.p2_timeout(5)

    configWriter.end()

    configReader = reader.ConfigReader()
    configReader.print()


# Device Network
# ==============
# IP:                      192.168.1.30
# Gateway:                 162.168.1.1
# Subnet:                  255.255.255.0
# MAC:                     38:3B:26:75:02:B0

# UART 1
# ======
# Network mode:             1
# Device port:              5000
# Destination port:         6969
# Destination IP:           192.168.1.148
# Baud rate:                9600
# Bits (stop, check, data): 1,4,8
# Timeout:                  2ms

# UART 2
# ======
# Network mode:             1
# Device port:              5000
# Destination port:         3000
# Destination IP:           192.168.1.70
# Baud rate:                115200
# Bits (stop, check, data): 1,4,8
# Timeout:                  2ms