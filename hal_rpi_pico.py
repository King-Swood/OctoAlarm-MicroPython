#pylint: disable=all
#type: ignore
import time
import sys
import machine

BUTTON_PIN = const(16)
LED_PIN = const(25)
LED_EXTERNAL_PIN = const(20)
led_onboard = None
led_external = None
button_pin = None

def init():
    global led_onboard
    led_onboard = machine.Pin(LED_PIN, machine.Pin.OUT)
    led_onboard.value(True)
    global led_external
    led_external = machine.PWM(machine.Pin(LED_EXTERNAL_PIN))
    led_external.freq(5000)
    led_external.duty_u16(0)
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

def get_us():
    return time.ticks_us()

def read_button():
    return not button_pin.value()

def set_led(value):
    global led_external
    led_external.duty_u16(int(value * 256))
    return

def set_heartbeat(value):
    led_onboard.value(value)
    return

def set_beeper(freq: int):
    # TODO: Need to add beeper functionality
    return

def allow_siren() -> bool:
    return True

