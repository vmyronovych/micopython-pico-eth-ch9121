import time
from pico_ch9121 import config
from pico_ch9121.config import reader, writer
from pico_ch9121.socket import ClientSocket

# CH9121 configuration
configWriter = writer.ConfigWriter()
configWriter.begin_config()
configWriter.enableDHCP() # Enables DHCP on CH9121 so the chip can automatically obtain IP address from your DHCP server (e.g. from home's router)
configWriter.gateway_ip("192.168.1.1") # Set here your's gateway ip address (e.g. router's ip)
configWriter.subnet_mask("255.255.255.0") # Set here your's subnet mask
configWriter.port1_network_mode(0x01) # TCP Client Mode
configWriter.end_config()

# Print current configuration of CH9121
configReader = reader.ConfigReader()
configReader.print()

# Prepare socket for communication
socket = ClientSocket("192.168.1.51", 6969) # Change ip and port here to the api and port of your TCP Server

# Send and read data to/from TCP Server
while True:
    response = socket.send("Hello from CH9121")
    print(response)
    time.sleep(10)