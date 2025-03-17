from Button import Button
import hal
from Heartbeat import Heartbeat
import Globals
from StartupPattern import StartupPattern

# if the file is called main.py, it will run automatically when the target device boots.

class App():
    def __init__(self):
        print("OctoAlarm MicroPython Version " + Globals.Version + "\n")

        self.button = Button(hal.read_button)
        self.heartbeat = Heartbeat(lambda x: hal.set_heartbeat(x))
        self.startupPattern = StartupPattern(self.startup_pattern_set)

    @staticmethod
    def startup_pattern_set(value):
        if value > 0:
            hal.set_led(255)
        else:
            hal.set_led(0)

    def loop(self):
        self.heartbeat.update()
        self.button.update()

        if not self.startupPattern.is_finished():
            self.startupPattern.update()
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
