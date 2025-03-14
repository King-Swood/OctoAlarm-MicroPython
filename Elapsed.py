import HAL

class Elapsed:
    last_time_ = HAL.get_ms()
        
    def restart(self):
        self.last_time_ = HAL.get_ms()
        
    def has_elapsed(self, ms):
        if (HAL.get_ms() - self.last_time_) >= ms:
            return True
        return False
        
    def has_elapsed_restart(self, ms):
        if self.has_elapsed(ms):
            self.restart()
            return True
        return False

