from __future__ import annotations
from enum import Enum, auto


class EColor(Enum):
    BLACK = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    PURPLE = auto()
    CYAN = auto()
    WHITE = auto()
    END = auto()
    BOLD = auto()
    DEFAULT = auto()


ecolor2terminalcolor_map: dict[EColor, str] = {
    EColor.BLACK: '\033[30m',
    EColor.RED: '\033[31m',
    EColor.GREEN: '\033[32m',
    EColor.YELLOW: '\033[33m',
    EColor.BLUE: '\033[34m',
    EColor.PURPLE: '\033[35m',
    EColor.CYAN: '\033[36m',
    EColor.WHITE: '\033[37m',
    EColor.END: '\033[0m',
    EColor.BOLD: '\038[1m',
    EColor.DEFAULT: '\033[0m',
}
