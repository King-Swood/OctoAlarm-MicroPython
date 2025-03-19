from elapsed import ElapsedUS

class Siren():
    STATE_INCREASING = 0
    STATE_PAUSE = 1
    STATE_SIZE = 2

    FREQ_LOW = 300
    FREQ_HIGH = 600

    # set_freq must be a callable that takes an int and returns None
    def __init__(self, set_freq, update_period_us: int):
        self.set_freq = set_freq
        self.update_period_us = update_period_us
        self.state = self.STATE_INCREASING
        self.last_state = self.STATE_SIZE
        self.current_freq = 0
        self.timer = ElapsedUS()
        self.pause_us = self.update_period_us * 0

    def update(self):
        first_time = self.state != self.last_state
        self.last_state = self.state

        if self.state == self.STATE_INCREASING:
            if first_time:
                self.current_freq = 0
                self.timer.restart()
            if self.timer.has_elapsed_restart(self.update_period_us):
                if self.current_freq < self.FREQ_HIGH:
                    self.current_freq += 1
                else:
                    self.state = self.STATE_PAUSE
            self.set_freq(self.current_freq)
        elif self.state == self.STATE_PAUSE:
            if first_time:
                self.timer.restart()
            if self.timer.has_elapsed(self.pause_us):
                self.state = self.STATE_INCREASING
