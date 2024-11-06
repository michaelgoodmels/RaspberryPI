import machine
import time

led_pin = machine.Pin ("LED", machine.Pin.OUT)

while True:
    led_pin.toggle()   # Toggle the led state
    time.sleep(3)       # wait for 1 second