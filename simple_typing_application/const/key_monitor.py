from enum import Enum


class EKeyMonitorType(Enum):
    SSHKEYBOARD: str = 'SSHKEYBOARD'
    PYNPUT: str = 'PYNPUT'
