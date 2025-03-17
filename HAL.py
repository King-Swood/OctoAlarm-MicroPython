import time
import sys

if (sys.platform == "linux") or (sys.platform == "win32"):
    # Full python
    from PySide6 import QtCore, QtWidgets, QtGui
    from PySide6.QtCore import QTimer

    sim = None

    class Sim (QtWidgets.QWidget):
        def __init__(self, main_loop):
            super().__init__()
            self.main_loop = main_loop
            self.layout = QtWidgets.QVBoxLayout(self)
            self.heartbeat = QtWidgets.QCheckBox("Heartbeat LED")
            self.layout.addWidget(self.heartbeat)
            self.button = QtWidgets.QPushButton("")
            self.layout.addWidget(self.button)

            self.timer = QTimer(self)
            self.timer.timeout.connect(lambda: self.main_loop())
            self.timer.start(0)
        
        def set_heartbeat(self, value):
            self.heartbeat.setChecked(value)


    def run(setup, loop):
        app = QtWidgets.QApplication([])

        global sim

        sim = Sim(loop)
        sim.show()

        setup()

        sys.exit(app.exec())

    def get_ms():
        return int(time.clock_gettime(time.CLOCK_MONOTONIC) * 1000.0)
    
    def read_button():
        return False
    
    def set_led(value):
        global sim
        sim.set_heartbeat(value)
else:
    # MicroPython
    import machine
    BUTTON_PIN = const(16)
    LED_PIN = const(25)
    led_onboard = None
    button_pin = None

    def init():
        global led_onboard
        led_onboard = machine.Pin(LED_PIN, machine.Pin.OUT)
        led_onboard.value(True)
        global button_pin
        button_pin = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
        return

    def get_ms():
        return time.ticks_ms()
    
    def read_button():
        return not button_pin.value()
    
    def set_led(value):
        led_onboard.value(value)
        return
