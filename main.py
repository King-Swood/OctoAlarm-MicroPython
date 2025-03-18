from button import Button
import hal
from heartbeat import Heartbeat
import app_globals
from startup_pattern import StartupPattern

# Since the file is called main.py, it will run automatically when the target device boots.

class App():
    def __init__(self):
        print("OctoAlarm MicroPython Version " + app_globals.VERSION + "\n")

        self.button = Button(hal.read_button)
        self.heartbeat = Heartbeat(lambda x: hal.set_heartbeat(x))
        self.startup_pattern = StartupPattern(self.startup_pattern_set)

    @staticmethod
    def startup_pattern_set(value):
        hal.set_led(255 if value > 0 else 0)
        hal.set_beeper(value)

    def loop(self):
        self.heartbeat.update()
        self.button.update()

        if not self.startup_pattern.is_finished():
            self.startup_pattern.update()
        else:
            hal.set_led(128)

        # if button.just_released():
        #     led_state = not led_state
        #     HAL.set_led(led_state)

        # if button.is_held(500):
        #     button.restart_held()
        #     led_state = not led_state
        #     HAL.set_led(led_state)

app: App

def setup():
    global app
    app = App()

def loop():
    global app
    app.loop()

hal.run(setup, loop)
