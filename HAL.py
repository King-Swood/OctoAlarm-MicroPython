import time
import sys

if (sys.platform == "linux") or (sys.platform == "win32"):
    # Full python

    def init():
        return

    def get_ms():
        return int(time.clock_gettime(time.CLOCK_MONOTONIC) * 1000.0)
    
    def read_button():
        return False
    
    def set_led(value):
        return
else:
    # MicroPython
    import machine
    BUTTON_PIN = const(16)
    LED_PIN = const(25)
    led_onboard = None
    button_pin = None

    def init():
        global led_onboard
        led_onboard = machine.Pin(LED_PIN, machine.Pin.OUT)
        led_onboard.value(True)
        global button_pin
        button_pin = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
        return

    def get_ms():
        return time.ticks_ms()
    
    def read_button():
        return not button_pin.value()
    
    def set_led(value):
        led_onboard.value(value)
        return
