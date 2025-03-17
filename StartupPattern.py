from Elapsed import Elapsed

class StartupPattern():
    DATA = [(1000,50),
            (0,50),
            (1000,50),
            (0,500)]

    def __init__(self, setFrequency):
        global DATA
        self.setFrequency = setFrequency
        self.elapsed = Elapsed()
        self.index = 0
        self.setFrequency(self.DATA[self.index][0])
        self.finished = False

    def update(self):
        if self.finished:
            return
        
        item = self.DATA[self.index]

        if self.elapsed.has_elapsed_restart(item[1]):
            self.index += 1
            if self.index >= len(self.DATA):
                self.finished = True
            else:
                item = self.DATA[self.index]
                self.setFrequency(item[0])

    def is_finished(self):
        return self.finished