import time
from machine import UART, Pin

OFF = 0x1

class ConfigWriter:
    def begin(self):
        self.__config_pin = Pin(14, Pin.OUT,Pin.PULL_UP)
        self.__uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
        time.sleep(0.1)
        self.__config_pin.value(0)
        time.sleep(0.1)
        self.__uart.read(self.__uart.any()) # cleanup old data on a line

    def end(self):
        self.__save_to_eeprom()
        self.__execute_config_and_reset()
        self.__leave_port_config_mode()
        self.__config_pin.value(1)
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
        return self.__write_ip(0x11, ip)

    def subnet_mask(self, mask):
        return self.__write_ip(0x12, mask)

    def gateway_ip(self, ip):
        return self.__write_ip(0x13, ip)

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
        return self.__write_one_byte_int(0x10, mode)

    def p1_device_port(self, port):
        return self.__write_two_bytes_int(0x14, port)

    def p1_dest_port(self, port):
        return self.__write_two_bytes_int(0x16, port)

    def p1_dest_ip(self, ip):
        return self.__write_ip(0x15, ip)

    # Set Baud Rate for serial port 1
    # for chip configuration mode the rate is always 9600
    # once chip exits configuration mode the baud rate will match the one set by this method
    def p1_baud_rate(self, baud_rate):
        return self.__write_four_bytes_int(0x21, baud_rate)

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
    def p1_timeout(self, timeout_ms):
        return self.__write_four_bytes_int(0x23, timeout_ms)

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
        return self.__write_one_byte_int(0x39, val)

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
        return self.__write_one_byte_int(0x40, mode)

    def p2_device_port(self, port):
        return self.__write_two_bytes_int(0x41, port)

    def p2_dest_port(self, port):
        return self.__write_two_bytes_int(0x43, port)

    def p2_dest_ip(self, ip):
        return self.__write_ip(0x42, ip)

    # Set Baud Rate for serial port 2
    def p2_baud_rate(self, baud_rate):
        return self.__write_four_bytes_int(0x44, baud_rate)
    
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
    def p2_timeout(self, timeout_ms):
        return self.__write_four_bytes_int(0x46, timeout_ms)

    # Save parameters to EEPROM
    def __save_to_eeprom(self):
        self.__write(0x0d)

    # Execute the configuration command, and Reset CH9121
    def __execute_config_and_reset(self):
        self.__write(0x0e)

    # Leave serial port configuration mode (Only on the serial port negotiating side Formula is valid)
    def __leave_port_config_mode(self):
        self.__write(0x5e)

    def __write_one_byte_int(self, cmd, val):
        self.__write(cmd, val.to_bytes(1, 'little'))

    def __write_two_bytes_int(self, cmd, val):
        self.__write(cmd, val.to_bytes(2, 'little'))
    
    def __write_four_bytes_int(self, cmd, val):
        self.__write(cmd, val.to_bytes(4, 'little'))

    def __write_ip(self, cmd, val):
        ip_bytes = []
        for ip_seg in val.split("."):
            ip_bytes.append(int(ip_seg).to_bytes(1, 'little')[0])
        self.__write(cmd, ip_bytes)

    def __write(self, cmd, val = None):
        full_cmd = [0x57, 0xab]
        full_cmd.append(cmd)

        if (val != None):
            for v in val:
                full_cmd.append(v)

        full_cmd_bytes = bytearray(full_cmd)
        print(full_cmd_bytes.hex(' ')) # configuration doesn't apply when remove this line :)
        self.__uart.write(full_cmd_bytes)
        time.sleep(.01) 

# Write, read and print configuration when this module is run as standalone python script
if __name__ == '__main__':
    from pico_ch9121.config import reader, writer

    cw = writer.ConfigWriter()
    cw.begin()

    cw.device_ip("192.168.0.27")
    cw.gateway_ip("192.168.0.1")
    cw.subnet_mask("255.255.0.127")

    cw.p1_tcp_client()
    cw.p1_device_port(5001)
    cw.p1_dest_port(6970)
    cw.p1_dest_ip("192.168.0.158")
    cw.p1_baud_rate(9600)
    cw.p1_uart_bits(1, 4, 8)
    cw.p1_timeout(5)

    cw.p2_on()
    cw.p2_tcp_server()
    cw.p2_device_port(5001)
    cw.p2_dest_port(6971)
    cw.p2_dest_ip("192.168.1.76")
    cw.p2_baud_rate(9600)
    cw.p2_uart_bits(1, 4, 8)
    cw.p2_timeout(5)

    cw.end()

    cr = reader.ConfigReader()
    cr.print_net()
    cr.print_p1()
    cr.print_p2()