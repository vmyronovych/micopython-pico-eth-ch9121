import time
from machine import UART, Pin
import configreader

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
CFG = Pin(14, Pin.OUT,Pin.PULL_UP)

print("begin")
CFG.value(0)
time.sleep(0.1)

configreader.printAll(uart0)

CFG.value(1)
time.sleep(0.1)
print("end")


