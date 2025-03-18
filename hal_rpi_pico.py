#pylint: disable=all
#type: ignore
import time
import sys
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

def run(setup, loop):
    init()
    setup()
    while True:
        loop()

def get_ms():
    return time.ticks_ms()

def read_button():
    return not button_pin.value()

def set_led(value):
    return

def set_heartbeat(value):
    led_onboard.value(value)
    return

def set_beeper(freq: int):
    # TODO: Need to add beeper functionality
    return
