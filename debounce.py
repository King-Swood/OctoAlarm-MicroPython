from elapsed import ElapsedMS

class Debounce:

    def __init__(self, initial_state = False, debounce_time = 50):
        self.state_ = initial_state
        self.debounce_time_ = debounce_time
        self.elapsed_ = ElapsedMS()

    def update(self, new_state):
        if new_state != self.state_:
            if self.elapsed_.has_elapsed_restart(self.debounce_time_):
                self.state_ = new_state
        else:
            self.elapsed_.restart()

    def state(self):
        return self.state_
