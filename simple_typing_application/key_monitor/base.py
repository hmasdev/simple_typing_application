from abc import ABC, abstractmethod
from typing import Callable

from ..const.keys import EMetaKey


class BaseKeyMonitor(ABC):

    def set_on_press_callback(
        self,
        callback: Callable[[EMetaKey | str | None], bool | None] | None,
    ):
        '''Set callback function for key press event.

        Args:
            callback (Callable[[EMetaKey | str | None], bool | None] | None):
                callback function for key press event.
                If the callback function returns False, the key monitor will stop.
        '''  # noqa
        self._on_press_callback = callback

    def set_on_release_callback(
        self,
        callback: Callable[[EMetaKey | str | None], bool | None] | None,
    ):
        '''Set callback function for key release event.

        Args:
            callback (Callable[[EMetaKey | str | None], bool | None] | None):
                callback function for key release event.
                If the callback function returns False, the key monitor will stop.
        '''  # noqa
        self._on_release_callback = callback

    @abstractmethod
    def start(self):
        raise NotImplementedError()

    @abstractmethod
    def stop(self):
        raise NotImplementedError()
