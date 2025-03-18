from enum import Enum, auto
from button import Button
import hal
from heartbeat import Heartbeat
import app_globals
from startup_pattern import StartupPattern
from led_pulse import LEDPulse
from siren import Siren

# Since the file is called main.py, it will run automatically when the target device boots.

class State(Enum):
    STARTUP = auto(),
    IDLE = auto(),
    ALARMING = auto(),
    SIZE = auto()

class App():

    def __init__(self):
        print("OctoAlarm MicroPython Version " + app_globals.VERSION + "\n")

        self.button = Button(hal.read_button)
        self.heartbeat = Heartbeat(lambda x: hal.set_heartbeat(x))
        self.startup_pattern: StartupPattern
        self.led_pulse: LEDPulse
        self.siren: Siren
        self.state = State.STARTUP
        self.last_state = State.SIZE

    @staticmethod
    def startup_pattern_set(value):
        hal.set_led(255 if value > 0 else 0)
        hal.set_beeper(value)

    def update(self):
        self.heartbeat.update()
        self.button.update()

        first_time = self.state != self.last_state
        self.last_state = self.state

        match self.state:
            case State.STARTUP:
                if first_time:
                    self.startup_pattern = StartupPattern(self.startup_pattern_set)
                if self.startup_pattern.is_finished():
                    self.state = State.IDLE
                else:
                    self.startup_pattern.update()
            case State.IDLE:
                if first_time:
                    hal.set_beeper(0)
                    hal.set_led(128)
                if self.button.just_released():
                    self.state = State.ALARMING
            case State.ALARMING:
                if first_time:
                    self.led_pulse = LEDPulse(lambda x: hal.set_led(x), 2000)
                    if hal.allow_siren():
                        self.siren = Siren(lambda x: hal.set_beeper(x), 3000)
                self.led_pulse.update()
                if hal.allow_siren():
                    self.siren.update()
                if self.button.just_released():
                    self.state = State.IDLE

app: App

def setup():
    global app
    app = App()

def loop():
    global app
    app.update()

hal.run(setup, loop)
