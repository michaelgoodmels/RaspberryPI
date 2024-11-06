from machine import Pin
import time

led_pin = machine.Pin ("LED", machine.Pin.OUT)

while True:
    led_pin.toggle()   # Toggle the led state
    time.sleep(3)       # wait for 1 second

    # GPIO-Pins definieren
    led_pin = Pin(15, Pin.OUT)
    button_pin = Pin(14, Pin.IN, Pin.PULL_UP)

    # Zustand der LED
    led_status = False

    # Hauptschleife
    try:
        while True:
            # Prüfen, ob der Taster gedrückt wurde
            if button_pin.value() == 0:  # LOW, wenn gedrückt
                led_status = not led_status
                led_pin.value(led_status)
                print("LED ist jetzt", "an" if led_status else "aus")

                # Entprellung
                time.sleep(0.3)

    except KeyboardInterrupt:
        pass  # Beenden mit CTRL+C in der Entwicklungsumgebung

