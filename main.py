from button import Button
import hal
from heartbeat import Heartbeat
import app_globals
from startup_pattern import StartupPattern
from led_pulse import LEDPulse
from siren import Siren
from theme_player import ThemePlayer
import theme

# Since the file is called main.py, it will run automatically when the target device boots.

BUTTON_HOLD_MS = 1000

class App():
    STATE_STARTUP = 0
    STATE_IDLE = 1
    STATE_ALARMING = 2
    STATE_TUNE = 3
    STATE_SIZE = 4

    def __init__(self):
        print("OctoAlarm MicroPython Version " + app_globals.VERSION + "\n")

        self.button = Button(hal.read_button)
        self.heartbeat = Heartbeat(lambda x: hal.set_heartbeat(x))
        self.startup_pattern: StartupPattern
        self.led_pulse: LEDPulse
        self.siren: Siren
        self.state = self.STATE_STARTUP
        self.last_state = self.STATE_SIZE
        self.released_in_theme_state = False
        self.theme_player: ThemePlayer

    @staticmethod
    def startup_pattern_set(value):
        hal.set_led(255 if value > 0 else 0)
        hal.set_beeper(value)

    def update(self):
        self.heartbeat.update()
        self.button.update()

        first_time = self.state != self.last_state
        self.last_state = self.state

        if self.state == self.STATE_STARTUP:
            if first_time:
                self.startup_pattern = StartupPattern(self.startup_pattern_set)
            if self.startup_pattern.is_finished():
                self.state = self.STATE_IDLE
            else:
                self.startup_pattern.update()
        elif self.state == self.STATE_IDLE:
            if first_time:
                hal.set_beeper(0)
                hal.set_led(128)
            if self.button.just_released():
                self.state = self.STATE_ALARMING
            if self.button.is_held(BUTTON_HOLD_MS):
                self.state = self.STATE_TUNE
        elif self.state == self.STATE_ALARMING:
            if first_time:
                self.led_pulse = LEDPulse(lambda x: hal.set_led(x), 2000)
                if hal.allow_siren():
                    self.siren = Siren(lambda x: hal.set_beeper(x), 3000)
            self.led_pulse.update()
            if hal.allow_siren():
                self.siren.update()
            if self.button.just_released():
                self.state = self.STATE_IDLE
        elif self.state == self.STATE_TUNE:
            if first_time:
                self.released_in_theme_state = False
                self.theme_player = ThemePlayer(lambda x: hal.set_beeper(x), theme.THEME)

            self.theme_player.update()

            if self.theme_player.is_finished():
                self.state = self.STATE_IDLE

            if self.button.just_released():
                if not self.released_in_theme_state:
                    self.released_in_theme_state = True
                else:
                    self.state = self.STATE_IDLE

app: App

def setup():
    global app
    app = App()

def loop():
    global app
    app.update()

hal.run(setup, loop)
