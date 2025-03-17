from Button import Button
import HAL
from Heartbeat import Heartbeat
import Globals
from StartupPattern import StartupPattern

# if the file is called main.py, it will run automatically when the target device boots.

button = None
heartbeat = None
startupPattern = None

def startup_pattern_set(value):
    if (value > 0):
        HAL.set_led(255)
    else:
        HAL.set_led(0)

def setup():
    global led_state
    global button
    global heartbeat
    global startupPattern

    print("OctoAlarm MicroPython Version " + Globals.Version + "\n")

    button = Button(HAL.read_button)
    heartbeat = Heartbeat(lambda x: HAL.set_heartbeat(x))
    startupPattern = StartupPattern(startup_pattern_set)

def loop():
    global led_state
    global button
    global heartbeat
    
    heartbeat.update()
    button.update()

    if not startupPattern.is_finished():
        startupPattern.update()
    else:
        HAL.set_led(128)
    
    # if button.just_released():
    #     led_state = not led_state
    #     HAL.set_led(led_state)
    
    # if button.is_held(500):
    #     button.restart_held()
    #     led_state = not led_state
    #     HAL.set_led(led_state)

HAL.run(setup, loop)