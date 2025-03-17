"""Main entry to the application."""

from Button import Button
import HAL

# if the file is called main.py, it will run automatically when the target device boots.

led_state = False
button = None

def setup():
    global led_state
    global button

    HAL.set_led(led_state)
    button = Button(HAL.read_button)

def loop():
    global led_state
    global button
    
    button.update()
    
    if button.just_released():
        led_state = not led_state
        HAL.set_led(led_state)
    
    if button.is_held(500):
        button.restart_held()
        led_state = not led_state
        HAL.set_led(led_state)

HAL.run(setup, loop)