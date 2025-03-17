import time
import sys
from PySide6 import QtCore, QtWidgets

class Sim (QtWidgets.QWidget):
    def __init__(self, main_loop):
        super().__init__()
        self.main_loop = main_loop
        layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(layout)
        self.heartbeat = QtWidgets.QCheckBox("Heartbeat LED")
        layout.addWidget(self.heartbeat)
        self.button = QtWidgets.QPushButton("")
        self.button.setStyleSheet('background-color: rgb(0,0,0)')
        layout.addWidget(self.button)
        self.resize(400,300)
        self.setWindowTitle("OctoAlarm Python Sim")

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda: self.main_loop())
        self.timer.start(0)

    def set_heartbeat(self, value):
        self.heartbeat.setChecked(value)

    def set_led(self, value):
        self.button.setStyleSheet(f'background-color: rgb({value},{value},{value})')
        return

    def read_button(self):
        return self.button.isDown()

def run(setup, loop):
    app = QtWidgets.QApplication([])

    global sim

    sim = Sim(loop)
    sim.show()

    setup()

    sys.exit(app.exec())

sim: Sim

def get_ms():
    return int(time.clock_gettime(time.CLOCK_MONOTONIC) * 1000.0)

def read_button():
    global sim
    return sim.read_button()

# TODO set_led will need to take an analog value.
def set_heartbeat(value):
    global sim
    sim.set_heartbeat(value)

def set_led(value):
    global sim
    sim.set_led(value)
