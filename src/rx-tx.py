from machine import UART, Pin
import time

uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
CFG = Pin(14, Pin.OUT,Pin.PULL_UP)
RST = Pin(17, Pin.OUT,Pin.PULL_UP)
CFG.value(1)
RST.value(1)

#print("writing to uart 1")
#uart0.write("hellow for uart 1")

while True:
    uart0.write("hello from pico")
    while uart0.any() > 0:    #Channel 0 is spontaneous and self-collecting
        rxData0 = uart0.read()
        uart0.write(rxData0)
        print(rxData0)
        time.sleep(10)
    time.sleep(10) 

