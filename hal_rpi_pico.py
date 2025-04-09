#pylint: disable=all
#type: ignore
import time
import sys
import machine

BEEPER_PIN = const(15)
BUTTON_PIN = const(16)
LED_EXTERNAL_PIN = const(20)
LED_ONBOARD_PIN = const(25)

led_onboard_pin = None
led_external_pwm = None
button_pin = None
beeper_pwm = None

def init():
    global led_onboard_pin
    led_onboard_pin = machine.Pin(LED_ONBOARD_PIN, machine.Pin.OUT)
    led_onboard_pin.value(True)
    global led_external_pwm
    led_external_pwm = machine.PWM(machine.Pin(LED_EXTERNAL_PIN))
    led_external_pwm.freq(5000)
    led_external_pwm.duty_u16(0)
    global button_pin
    button_pin = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    global beeper_pwm
    beeper_pwm = machine.PWM(machine.Pin(BEEPER_PIN))
    beeper_pwm.duty_u16(0)
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
    global led_external_pwm
    led_external_pwm.duty_u16(int(value * 256))
    return

def set_heartbeat(value):
    led_onboard_pin.value(value)
    return

def set_beeper(freq: int):
    if freq < 100:
        beeper_pwm.freq(5000)
        beeper_pwm.duty_u16(0)
    else:
        beeper_pwm.freq(freq)
        beeper_pwm.duty_u16(65535 >> 1)
    return

def allow_siren() -> bool:
    return True
