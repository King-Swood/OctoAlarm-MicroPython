import hal

class _Elapsed:
    def __init__(self):
        self.last_time_ = self.get_time()

    def restart(self):
        self.last_time_ = self.get_time()

    def has_elapsed(self, ms):
        if (self.get_time() - self.last_time_) >= ms:
            return True
        return False

    def has_elapsed_restart(self, ms):
        if self.has_elapsed(ms):
            self.restart()
            return True
        return False

    def get_time(self) -> int:
        return 0

class ElapsedMS(_Elapsed):
    def get_time(self) -> int:
        return hal.get_ms()

class ElapsedUS(_Elapsed):
    def get_time(self) -> int:
        return hal.get_us()
