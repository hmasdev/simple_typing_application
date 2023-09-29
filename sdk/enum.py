from enum import auto, Enum


class ETask(Enum):
    CREATE = auto()
    INTEGRATE = auto()


class EComponent(Enum):
    KEY_MONITOR = auto()
    SENTENCE_GENERATOR = auto()
    UI = auto()
