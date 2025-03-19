from collections.abc import Callable
from enum import Enum, auto
from elapsed import ElapsedUS

class Siren():
    class State(Enum):
        INCREASING = auto(),
        PAUSE = auto(),
        SIZE = auto()

    FREQ_LOW = 300
    FREQ_HIGH = 600

    def __init__(self, set_freq: Callable[[int],None], update_period_us: int):
        self.set_freq = set_freq
        self.update_period_us = update_period_us
        self.state = self.State.INCREASING
        self.last_state = self.State.SIZE
        self.current_freq = 0
        self.timer = ElapsedUS()
        self.pause_us = self.update_period_us * 0

    def update(self):
        first_time = self.state != self.last_state
        self.last_state = self.state

        if self.state == self.State.INCREASING:
            if first_time:
                self.current_freq = 0
                self.timer.restart()
            if self.timer.has_elapsed_restart(self.update_period_us):
                if self.current_freq < self.FREQ_HIGH:
                    self.current_freq += 1
                else:
                    self.state = self.State.PAUSE
            self.set_freq(self.current_freq)
        elif self.state == self.State.PAUSE:
            if first_time:
                self.timer.restart()
            if self.timer.has_elapsed(self.pause_us):
                self.state = self.State.INCREASING
