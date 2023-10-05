from logging import getLogger, Logger
from typing import Callable
from pynput import keyboard
from .base import BaseKeyMonitor
from ..const.keys import EMetaKey


class PynputBasedKeyMonitor(BaseKeyMonitor):

    def __init__(
        self,
        logger: Logger = getLogger(__name__),
    ):
        self._listener: keyboard.Listener | None = None
        self._on_press_callback: Callable[[EMetaKey | str | None], bool | None] | None = None  # noqa
        self._on_release_callback: Callable[[EMetaKey | str | None], bool | None] | None = None  # noqa
        self._logger = logger

    def start(self):
        self._listener = keyboard.Listener(
            on_press=self._on_press_callback_wrapper,
            on_release=self._on_release_callback_wrapper,
        )
        self._listener.start()
        self._listener.join()

    def stop(self):

        if self._listener is None:
            self._logger.warning(f'{self.__class__.__name__}() has not been started.')  # noqa
            return

        self._listener.stop()
        del self._listener
        self._listener = None

    def _clean_key(
        self,
        key: keyboard.Key | keyboard.KeyCode | None,
    ) -> EMetaKey | str | None:
        self._logger.debug(f'key: {key}')
        if isinstance(key, keyboard.Key):
            if key == keyboard.Key.esc:
                return EMetaKey.ESC
            elif key == keyboard.Key.tab:
                return EMetaKey.TAB
            elif key == keyboard.Key.space:
                return ' '
            else:
                self._logger.warning(f'key: {key} is not supported.')
                return None
        elif isinstance(key, keyboard.KeyCode):
            return key.char
        else:
            self._logger.warning(f'key: {key} is not supported.')
            return None

    def _on_press_callback_wrapper(
        self,
        key: keyboard.Key | keyboard.KeyCode | None,
    ):
        self._logger.debug(f'pressed key: {key}')
        cleaned_key = self._clean_key(key)

        if self._on_press_callback is None:
            self._logger.warning(f'{self.__class__.__name__}._on_press_callback is None.')  # noqa
            return

        return self._on_press_callback(cleaned_key)

    def _on_release_callback_wrapper(
        self,
        key: keyboard.Key | keyboard.KeyCode | None,
    ):
        self._logger.debug(f'released key: {key}')
        cleaned_key = self._clean_key(key)

        if self._on_release_callback is None:
            self._logger.warning(f'{self.__class__.__name__}._on_release_callback is None.')  # noqa
            return

        return self._on_release_callback(cleaned_key)
