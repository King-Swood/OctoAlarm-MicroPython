import sys

if (sys.platform == "linux") or (sys.platform == "win32"):
    # Simulator
    import hal_sim as hal_impl
else:
    # MicroPython
    import hal_rpi_pico as hal_impl

def run(setup, loop):
    hal_impl.run(setup, loop)

def get_ms() -> int:
    return hal_impl.get_ms()

def get_us() -> int:
    return hal_impl.get_us()

def read_button() -> bool:
    return hal_impl.read_button()

def set_heartbeat(value: bool):
    hal_impl.set_heartbeat(value)

def set_led(value: int):
    hal_impl.set_led(value)

def set_beeper(freq: int):
    hal_impl.set_beeper(freq)

def allow_siren() -> bool:
    return hal_impl.allow_siren()
