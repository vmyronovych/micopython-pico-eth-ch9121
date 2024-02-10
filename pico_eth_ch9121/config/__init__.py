from machine import UART, Pin

resetPin = Pin(17, Pin.OUT,Pin.PULL_UP)
resetPin.value(1)
print("Initialized")