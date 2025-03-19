from collections.abc import Callable
from elapsed import ElapsedUS

class LEDPulse():
    STATE_INCREASING = 0
    STATE_PAUSEBRIGHT = 1
    STATE_DECREASING = 2
    STATE_PAUSEOFF = 3
    STATE_SIZE = 4

    MAX_PWM = 255

    def __init__(self, set_output: Callable[[int],None], update_period_us: int):
        self.set_output = set_output
        self.update_period_us = update_period_us
        self.state = self.STATE_INCREASING
        self.last_state = self.STATE_SIZE
        self.pwm_value = 0
        self.timer = ElapsedUS()
        self.pause_us = self.update_period_us * 100

    def update(self):
        first_time = self.state != self.last_state
        self.last_state = self.state

        if self.state == self.STATE_INCREASING:
            if first_time:
                self.pwm_value = 0
                self.timer.restart()
            if self.timer.has_elapsed_restart(self.update_period_us):
                if self.pwm_value < self.MAX_PWM:
                    self.pwm_value += 1
                else:
                    self.state = self.STATE_PAUSEBRIGHT
            self.set_output(self.pwm_value)
        elif self.state == self.STATE_PAUSEBRIGHT:
            if first_time:
                self.timer.restart()
            if self.timer.has_elapsed(self.pause_us):
                self.state = self.STATE_DECREASING
        elif self.state == self.STATE_DECREASING:
            if first_time:
                self.pwm_value = self.MAX_PWM
                self.timer.restart()
            if self.timer.has_elapsed_restart(self.update_period_us):
                if self.pwm_value > 0:
                    self.pwm_value -= 1
                else:
                    self.state = self.STATE_PAUSEOFF
            self.set_output(self.pwm_value)
        elif self.state == self.STATE_PAUSEOFF:
            if first_time:
                self.timer.restart()
            if self.timer.has_elapsed(self.pause_us):
                self.state = self.STATE_INCREASING
