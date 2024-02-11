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
cw.p1_baud_rate(115200)
cw.end()

# Print current configuration of CH9121
cr = reader.ConfigReader()
cr.print_net()
cr.print_p1()

print(f'ELAPSED: {(time.time_ns() - start)/1000000000}')

# Prepare socket for communication
socket = TcpClientSocket("192.168.1.51", 8080) # Change ip and port here to the ip and port of your TCP Server

# Send and receive data every 2 seconds
while True:
    request = "GET /ch9221 HTTP/1.1\r\n\r\n"
    print(f">> {request.replace("\r", "\\r").replace("\n", "\\n")} | {socket.send_utf8_str(request)}")
    i = 0
    print(socket.receive_sync(5))
    time.sleep(2)