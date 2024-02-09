import time
from machine import UART, Pin

class ConfigWriter:
    def begin_config(self):
        self.__configPin = Pin(14, Pin.OUT,Pin.PULL_UP)
        self.__uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))        
        time.sleep(0.1)
        self.__configPin.value(0)
        time.sleep(0.1)
        self.__uart.read(self.__uart.any()) # cleanup old data on a line

    def end_config(self):
        self.__save_to_eeprom()
        self.__execute_config_and_reset()
        self.__leave_port_config_mode()
        self.__configPin.value(1)
        time.sleep(0.1)

    def device_ip(self, ip):
        return self.__writeIp(0x11, ip)
    
    def subnet_mask(self, ipMask):
        return self.__writeIp(0x12, ipMask)

    def gateway_ip(self, ip):
        return self.__writeIp(0x13, ip)
    
    # Possible values: 
    #   0x00: TCP server
    #   0x01: TCP client
    #   0x02: UDP server
    #   0x03: UDP client
    def port1_network_mode(self, mode):
        return self.__writeOneByteInt(0x10, mode)
    
    def port1_device_port_number(self, portNumber):
        return self.__writeTwoBytesInt(0x14, portNumber)
    
    def port1_destination_port_number(self, portNumber):
        return self.__writeTwoBytesInt(0x16, portNumber)
    
    def port1_destination_ip(self, ip):
        return self.__writeIp(0x15, ip)
    
    # UART0 serial port Baud Rate
    # for chip configuration mode the rate is always 9600
    # once chip exits configuration mode the baud rate will match the one set by this method
    def port1_uart_baud_rate(self, baudRate):
        return self.__writeFourBytesInt(0x21, baudRate)
    
    # Set port 1 serial port calibration bit, data bit, stop bit
    # 0x01 0x04 0x08
    # (1stop,noproofreading,8data)
    # Check:: 
    #   0x00: even
    #   0x01: add
    #   0x02: mark
    #   0x03: Space
    #   0x04: None
    def port1_uart_bits(self, stop, pairty, data):
        return self.__write(0x22, [stop, pairty, data])
    
    # Serial port's timeout time in milliseconds
    # 0x01 (Serial timeout 1*5ms)
    def port1_timeout(self, timeoutMs):
        return self.__writeFourBytesInt(0x23, timeoutMs)
    
    # Turn on/off port 2
    # 0x01: open
    # 0x00: close
    def port2_enabled(self, enabled):
        return self.__writeOneByteInt(0x39, enabled)

    # Possible values: 
    #   0x00: TCP server
    #   0x01: TCP client
    #   0x02: UDP server
    #   0x03: UDP client
    def port2_network_mode(self, mode):
        return self.__writeOneByteInt(0x40, mode)
    
    def port2_device_port_number(self, portNumber):
        return self.__writeTwoBytesInt(0x41, portNumber)
    
    def port2_destination_port_number(self, portNumber):
        return self.__writeTwoBytesInt(0x43, portNumber)
    
    def port2_destination_ip(self, ip):
        return self.__writeIp(0x42, ip)
    
    # UART1 serial port Baud Rate
    def port2_uart_baud_rate(self, baudRate):
        return self.__writeFourBytesInt(0x44, baudRate)
    
    # Set port 1 serial port calibration bit, data bit, stop bit
    # 0x01 0x04 0x08
    # (1stop,noproofreading,8data)
    # Check:: 
    #   0x00: even
    #   0x01: add
    #   0x02: mark
    #   0x03: Space
    #   0x04: None
    def port2_uart_bits(self, stop, pairty, data):
        return self.__write(0x45, [stop, pairty, data])
    
    # Serial port's timeout time in milliseconds
    # 0x01 (Serial timeout 1*5ms)
    def port2_timeout(self, timeoutMs):
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
    configWriter.begin_config()

    configWriter.device_ip("192.168.0.27")
    configWriter.gateway_ip("192.168.0.1")
    configWriter.subnet_mask("255.255.0.127")

    configWriter.port1_network_mode(0x01)
    configWriter.port1_device_port_number(5001)
    configWriter.port1_destination_port_number(6970)
    configWriter.port1_destination_ip("192.168.0.158")
    configWriter.port1_uart_baud_rate(9600)
    configWriter.port1_uart_bits(1, 4, 8)
    configWriter.port1_timeout(5)

    configWriter.port2_enabled(1)
    configWriter.port2_network_mode(2)
    configWriter.port2_device_port_number(5001)
    configWriter.port2_destination_port_number(6971)
    configWriter.port2_destination_ip("192.168.1.76")
    configWriter.port2_uart_baud_rate(9600)
    configWriter.port2_uart_bits(1, 4, 8)
    configWriter.port2_timeout(5)

    configWriter.end_config()

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