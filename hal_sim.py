import time
import sys
from PySide6 import QtCore, QtWidgets
import numpy as np
import simpleaudio as sa

class Sim (QtWidgets.QWidget):
    def __init__(self, main_loop):
        super().__init__()
        self.main_loop = main_loop
        self.sin_wave = None
        self.beep_instance = None
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
        if (freq <= 0):
            sa.stop_all()
            self.beep_instance = None
            return

        sa.stop_all()
        sample_rate = 44100
        t_mult = 0.25
        t = np.linspace(0, t_mult, int(t_mult * sample_rate), False)
        self.sin_wave = np.sin(freq * t * 2 * np.pi)
        self.sin_wave *= 32767 / np.max(np.abs(self.sin_wave))
        self.sin_wave = self.sin_wave.astype(np.int16)
        self.beep_instance = sa.play_buffer(self.sin_wave, 1, 2, sample_rate)
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

def get_us() -> int:
    return int(time.clock_gettime(time.CLOCK_MONOTONIC) * 1000000.0)

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

def allow_siren() -> bool:
    return False