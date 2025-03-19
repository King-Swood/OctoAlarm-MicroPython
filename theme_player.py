from collections.abc import Callable
from elapsed import ElapsedMS

# A theme is a list of tuple[int,int]
# The first item in the tuple is the frequency.
# The second item in the tuple is the milliseconds.

QUAVER = 350
SEMI_QUAVER = 150

NOTE_E5 = 659
NOTE_G5 = 783
NOTE_B4 = 493
NOTE_D5 = 587
NOTE_GS5 = 830
NOTE_A5 = 880
NOTE_AS5 = 932
NOTE_B5 = 987
NOTE_C6 = 1046
NOTE_D6 = 1174
NOTE_DS6 = 1244
NOTE_E6 = 1318

class ThemePlayer:
    STATE_PLAY_NOTE = 0
    STATE_PAUSE = 1
    STATE_FINISHED = 2
    STATE_SIZE = 3

    PAUSE_TIME = 50

    def __init__(self, set_freq: Callable[[int], None], theme: list[tuple[int, int]]):
        self.set_freq = set_freq
        self.theme = theme
        self.elapsed = ElapsedMS()
        self.index = 0
        self.state = self.STATE_PLAY_NOTE
        self.last_state = self.STATE_SIZE

    def update(self):
        first_time = self.state != self.last_state
        self.last_state = self.state

        if self.state == self.STATE_PLAY_NOTE:
            if first_time:
                self.elapsed.restart()
                self.set_freq(self.theme[self.index][0])

            if self.elapsed.has_elapsed_restart(self.theme[self.index][1]):
                self.index += 1
                self.state = self.STATE_PAUSE
        elif self.state == self.STATE_PAUSE:
                if first_time:
                    self.elapsed.restart()
                    self.set_freq(0)
                if self.elapsed.has_elapsed_restart(self.PAUSE_TIME):
                    if self.index >= len(self.theme):
                        self.state = self.STATE_FINISHED
                    else:
                        self.state = self.STATE_PLAY_NOTE

    def is_finished(self):
        return self.state == self.STATE_FINISHED
