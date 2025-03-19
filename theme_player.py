from collections.abc import Callable
from enum import Enum, auto
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
    class State(Enum):
        PLAY_NOTE = auto(),
        PAUSE = auto(),
        FINISHED = auto(),
        SIZE = auto()

    PAUSE_TIME = 50

    def __init__(self, set_freq: Callable[[int], None], theme: list[tuple[int, int]]):
        self.set_freq = set_freq
        self.theme = theme
        self.elapsed = ElapsedMS()
        self.index = 0
        self.state = self.State.PLAY_NOTE
        self.last_state = self.State.SIZE

    def update(self):
        first_time = self.state != self.last_state
        self.last_state = self.state

        match self.state:
            case self.State.PLAY_NOTE:
                if first_time:
                    self.elapsed.restart()
                    self.set_freq(self.theme[self.index][0])

                if self.elapsed.has_elapsed_restart(self.theme[self.index][1]):
                    self.index += 1
                    self.state = self.State.PAUSE
            case self.State.PAUSE:
                if first_time:
                    self.elapsed.restart()
                    self.set_freq(0)
                if self.elapsed.has_elapsed_restart(self.PAUSE_TIME):
                    if self.index >= len(self.theme):
                        self.state = self.State.FINISHED
                    else:
                        self.state = self.State.PLAY_NOTE

    def is_finished(self):
        return self.state == self.State.FINISHED
