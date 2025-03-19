from collections.abc import Callable
from enum import Enum, auto
from elapsed import ElapsedUS

class LEDPulse():
    class State(Enum):
        INCREASING = auto(),
        PAUSEBRIGHT = auto(),
        DECREASING = auto(),
        PAUSEOFF = auto(),
        SIZE = auto()

    MAX_PWM = 255

    def __init__(self, set_output: Callable[[int],None], update_period_us: int):
        self.set_output = set_output
        self.update_period_us = update_period_us
        self.state = self.State.INCREASING
        self.last_state = self.State.SIZE
        self.pwm_value = 0
        self.timer = ElapsedUS()
        self.pause_us = self.update_period_us * 100

    def update(self):
        first_time = self.state != self.last_state
        self.last_state = self.state

        if self.state == self.State.INCREASING:
            if first_time:
                self.pwm_value = 0
                self.timer.restart()
            if self.timer.has_elapsed_restart(self.update_period_us):
                if self.pwm_value < self.MAX_PWM:
                    self.pwm_value += 1
                else:
                    self.state = self.State.PAUSEBRIGHT
            self.set_output(self.pwm_value)
        elif self.state == self.State.PAUSEBRIGHT:
            if first_time:
                self.timer.restart()
            if self.timer.has_elapsed(self.pause_us):
                self.state = self.State.DECREASING
        elif self.state == self.State.DECREASING:
            if first_time:
                self.pwm_value = self.MAX_PWM
                self.timer.restart()
            if self.timer.has_elapsed_restart(self.update_period_us):
                if self.pwm_value > 0:
                    self.pwm_value -= 1
                else:
                    self.state = self.State.PAUSEOFF
            self.set_output(self.pwm_value)
        elif self.state == self.State.PAUSEOFF:
            if first_time:
                self.timer.restart()
            if self.timer.has_elapsed(self.pause_us):
                self.state = self.State.INCREASING
