from elapsed import Elapsed

class Heartbeat():
    def __init__(self, set_state):
        self.set_state = set_state
        self.set_state(False)
        self.state = False
        self.elapsed = Elapsed()

    def update(self):
        if self.elapsed.has_elapsed_restart(1000):
            self.state = not self.state
            self.set_state(self.state)
