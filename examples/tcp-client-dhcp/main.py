import time
from pico_eth_ch9121 import config
from pico_eth_ch9121.config import reader, writer
from pico_eth_ch9121.tcp_client_socket import TcpClientSocket

start = time.time_ns()

# ch9121 configuration
cw = writer.ConfigWriter()
cw.begin()
cw.dhcp_on() # Enable DHCP on CH9121 so the chip can automatically obtain IP address from your DHCP server (e.g. from home's router)
cw.gateway_ip("192.168.1.1") # Set here your's gateway ip address (e.g. router's ip)
cw.subnet_mask("255.255.255.0") # Set here your's subnet mask
cw.p1_tcp_client() # TCP Client Mode
cw.end()

# Print current configuration of CH9121
cr = reader.ConfigReader()
cr.print_net()
cr.print_p1()

print(f'ELAPSED: {(time.time_ns() - start)/1000000000}')

# Prepare socket for communication
socket = TcpClientSocket("192.168.1.51", 6969) # Change ip and port here to the ip and port of your TCP Server

# Send and receive data every 2 seconds
while True:
    print(f'tx:{socket.send_utf8_str("Hello from CH9121")}|rx:{socket.receive_sync(0.01)}')
    time.sleep(2)