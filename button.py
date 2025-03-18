from elapsed import ElapsedMS
from debounce import Debounce

class Button:
    def __init__(self, get_state):
        self.get_state_ = get_state
        self.pressed_ = False
        self.last_pressed_ = False
        self.debounced_state_ = Debounce()
        self.pressed_timer_ = ElapsedMS()

    def update(self):
        self.last_pressed_ = self.pressed_
        self.debounced_state_.update(self.get_state_())
        self.pressed_ = self.debounced_state_.state()
        if self.just_pressed():
            self.pressed_timer_.restart()

    def is_pressed(self):
        return self.pressed_

    def is_released(self):
        return not self.pressed_

    def just_changed(self):
        return self.pressed_ != self.last_pressed_

    def just_pressed(self):
        return self.just_changed() and self.is_pressed()

    def just_released(self):
        return self.just_changed() and self.is_released()

    def is_held(self, hold_time_ms):
        return self.is_pressed() and self.pressed_timer_.has_elapsed(hold_time_ms)

    def restart_held(self):
        self.pressed_timer_.restart()
