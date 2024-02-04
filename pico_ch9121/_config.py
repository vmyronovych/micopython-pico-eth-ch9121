from machine import UART, Pin
import time

uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

CFG = Pin(14, Pin.OUT,Pin.PULL_UP)
RST = Pin(17, Pin.OUT,Pin.PULL_UP)
RST.value(1)

MODE = 1  #0:TCP Server 1:TCP Client 2:UDP Server 3:UDP Client
GATEWAY = (162, 168, 1, 1)   # GATEWAY
TARGET_IP = (192, 168, 1, 148)# TARGET_IP
LOCAL_IP = (192, 168, 1, 30)    # LOCAL_IP
SUBNET_MASK = (255,255,255,0) # SUBNET_MASK
LOCAL_PORT1 = 5000             # LOCAL_PORT1
LOCAL_PORT2 = 4000             # LOCAL_PORT2
TARGET_PORT = 6969            # TARGET_PORT
BAUD_RATE = 9600            # BAUD_RATE

print("begin")
CFG.value(0)
time.sleep(0.1)
uart0.write(b'\x57\xab\x10'+MODE.to_bytes(1, 'little'))
time.sleep(0.1)
uart0.write(b'\x57\xab\x11'+bytes(bytearray(LOCAL_IP)))
time.sleep(0.1)
uart0.write(b'\x57\xab\x12'+bytes(bytearray(SUBNET_MASK)))
time.sleep(0.1)
uart0.write(b'\x57\xab\x13'+bytes(bytearray(GATEWAY)))
time.sleep(0.1)
uart0.write(b'\x57\xab\x14'+LOCAL_PORT1.to_bytes(2, 'little'))
time.sleep(0.1)
uart0.write(b'\x57\xab\x15'+bytes(bytearray(TARGET_IP)))
time.sleep(0.1)
uart0.write(b'\x57\xab\x16'+TARGET_PORT.to_bytes(2, 'little'))

time.sleep(0.1)
uart0.write(b'\x57\xab\x21'+BAUD_RATE.to_bytes(4, 'little'))
time.sleep(0.1)
uart0.write(b'\x57\xab\x0D')
time.sleep(0.1)
uart0.write(b'\x57\xab\x0E')
time.sleep(0.1)
uart0.write(b'\x57\xab\x5E')
time.sleep(0.1)
CFG.value(1)
time.sleep(0.1)
print("end")
