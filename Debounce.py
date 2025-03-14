import time
from Elapsed import Elapsed

class Debounce:
    state_ = False
    debounce_time_ = 50
    elapsed_ = Elapsed()
    
    def __init__(self, initial_state = False, debounce_time = 50):
        self.state_ = initial_state
        self.debounce_time_ = debounce_time
        
    def update(self, new_state):
        if new_state != self.state_:
            if self.elapsed_.has_elapsed_restart(self.debounce_time_):
                self.state_ = new_state
        else:
            self.elapsed_.restart()
    
    def state(self):
        return self.state_
