'''Heartbeat class'''

from Elapsed import Elapsed

class Heartbeat():
    def __init__(self, setState):
        self.setState = setState
        self.setState(False)
        self.state = False
        self.elapsed = Elapsed()

    def update(self):
        if self.elapsed.has_elapsed_restart(1000):
            self.state = not self.state
            self.setState(self.state)