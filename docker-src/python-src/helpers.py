from microcontroller import Pin
from copy import deepcopy

try:
    import board
except NotImplementedError:
    board = {}

VALID_PINS = dir(board)


class create_dot_dict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __deepcopy__(self, memo=None):
        return create_dot_dict(deepcopy(dict(self), memo=memo))


def convert_str_to_pin(pin_name: str) -> Pin:
    """Attempts to convert a pin name from string to a CircuitPython Pin object"""
    if pin_name is None:
        return None
    try:
        pin_index = VALID_PINS.index(pin_name)
        return getattr(board, VALID_PINS[pin_index])
    except ValueError:
        raise ValueError(f"The provided pin ({pin_name}) could not be found")


def convert_str_to_addr(addr: str) -> int:
    """Attempts to convert an address string to an (int) address"""
    try:
        return int(addr, 2)
    except ValueError:
        pass
    try:
        return int(addr, 16)
    except ValueError:
        pass
    raise ValueError(f"The provided address ({addr}) cannot be interpreted")

def calculate_list_average(l: list) -> float:
    return sum(l)/len(l)


_SAFE_MODULES = frozenset(
    ("board", "busio", "aesio", "analogio", "digitalio", "microcontroller", "pulseio"),
)


def safe_import(name, *args, **kwargs):
    if name not in _SAFE_MODULES or not name.startswith("adafruit"):
        raise Exception(f"Disallowed module")
    return __import__(name, *args, **kwargs)
