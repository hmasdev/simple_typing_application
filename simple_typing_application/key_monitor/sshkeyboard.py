from __future__ import annotations
from collections import deque
from logging import getLogger, Logger
from threading import Thread
from typing import Callable
from sshkeyboard import listen_keyboard, stop_listening
from .base import BaseKeyMonitor
from ..const.keys import EMetaKey


class SSHKeyboardBasedKeyMonitor(BaseKeyMonitor):
    def __init__(
        self,
        logger: Logger = getLogger(__name__),
    ):
        self._on_press_callback: Callable[[EMetaKey | str | None], bool | None] | None = None  # noqa
        self._on_release_callback: Callable[[EMetaKey | str | None], bool | None] | None = None  # noqa
        self._logger = logger

        self.__thread: Thread | None = None
        self.__keys_queue: deque = deque()

    def start(self):
        self.__thread = Thread(
            target=listen_keyboard,
            kwargs=dict(
                on_press=self._on_press_callback_wrapper,
                on_release=self._on_release_callback_wrapper,
            ),
        )
        self.__thread.start()
        self.__thread.join()

    def stop(self):
        if self.__thread is None:
            self._logger.warning(f"{self.__class__.__name__}() has not been started.")  # noqa
            return

        # send stop command
        stop_listening()
        # reset keys queue
        self._reset_keys_queue()
        # reset thread
        self.__thread = None

    def _reset_keys_queue(self):
        self.__keys_queue.clear()

    def _clean_key(self, key: str) -> EMetaKey | str | None:
        if len(key) == 1:
            return key
        elif key.lower() == "tab":
            return EMetaKey.TAB
        elif key.lower() == "esc":
            return EMetaKey.ESC
        elif key.lower() == "space":
            return " "
        else:
            self._logger.warning(f"Invalid key: {key}")
            return None

    def _on_press_callback_wrapper(self, key: str):
        self._logger.debug(f"pressed key: {key}")
        # record key
        if len(key) == 1:
            # NOTE: key can be two or more characters when it is a special key like "tab"  # noqa
            self.__keys_queue.append(key)
        # preprocess
        key_ = self._clean_key(key)
        # callback
        if self._on_press_callback is None:
            self._logger.warning(f"{self.__class__.__name__}._on_press_callback is None.")  # noqa
            return
        return self._on_press_callback(key_)

    def _on_release_callback_wrapper(self, key: str):
        self._logger.debug(f"released key: {key}")
        if self._on_release_callback is None:
            self._logger.warning(f"{self.__class__.__name__}._on_release_callback is None.")  # noqa
            return
        return self._on_release_callback(self._clean_key(key))
