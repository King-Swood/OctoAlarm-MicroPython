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

    def set_heartbeat(self, value: bool):
        self.heartbeat.setChecked(value)

    def set_led(self, value: int):
        self.button.setStyleSheet(f'background-color: rgb({value},{value},{value})')
        return

    def read_button(self) -> bool:
        return self.button.isDown()

    def set_beeper(self, freq: int):
        return

def run(setup, loop):
    app = QtWidgets.QApplication([])

    global sim

    sim = Sim(loop)
    sim.show()

    setup()

    sys.exit(app.exec())

sim: Sim

def get_ms() -> int:
    return int(time.clock_gettime(time.CLOCK_MONOTONIC) * 1000.0)

def read_button() -> bool:
    global sim
    return sim.read_button()

def set_heartbeat(value: bool):
    global sim
    sim.set_heartbeat(value)

def set_led(value: int):
    global sim
    sim.set_led(value)

def set_beeper(freq: int):
    global sim
    sim.set_beeper(freq)
