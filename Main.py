from Button import Button
import HAL

HAL.init()

led_state = False
HAL.set_led(led_state)

button = Button(lambda: HAL.read_button())

while True:
    button.update()
    
    if button.just_released():
        led_state = not led_state
        HAL.set_led(led_state)
    
    if button.is_held(500):
        button.restart_held()
        led_state = not led_state
        HAL.set_led(led_state)

