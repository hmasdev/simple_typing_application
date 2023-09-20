import asyncio
from copy import deepcopy
from datetime import datetime as dt
import json
from logging import getLogger, Logger
import os
import queue

from pynput.keyboard import KeyCode, Key, Listener

from .const import ASCII_CHARS
from .const.color import EColor
from .models.output_model import OutputModel
from .models.record_model import RecordModel
from .models.typing_target_model import TypingTargetModel
from .sentence_generator.base import BaseSentenceGenerator
from .ui.base import BaseUserInterface


# TODO: add various keyboard input monitor.

class TypingGame:

    _typing_target_title_color = EColor.YELLOW
    _typing_target_text_color = EColor.DEFAULT
    _correct_user_input_color = EColor.GREEN
    _incorrect_user_input_color = EColor.RED
    _system_anounce_color = EColor.YELLOW

    def __init__(
        self,
        sentence_generator: BaseSentenceGenerator,
        ui: BaseUserInterface,
        record_direc: str,
        logger: Logger = getLogger(__name__),
    ):
        self._sentence_generator = sentence_generator
        self._ui = ui
        self._record_direc = record_direc
        self._logger = logger

        os.makedirs(self._record_direc, exist_ok=True)

    def start(self):
        asyncio.run(self._main_loop())

    async def _main_loop(self):

        # initialize
        task1 = asyncio.create_task(self._sentence_generator.generate())
        typing_target: TypingTargetModel = await task1  # type: ignore

        # typing start
        while True:
            self._logger.debug(f'typing target: {typing_target}')
            self._show_typing_target(typing_target)
            task1 = asyncio.create_task(self._sentence_generator.generate())
            task2 = asyncio.create_task(self._typing_step(typing_target))
            typing_target, _ = await asyncio.gather(task1, task2)

    def _show_typing_target(self, typing_target: TypingTargetModel):
        self._ui.show_typing_target(
            typing_target.text,
            title='Typing Target',
            color=self._typing_target_text_color,
            title_color=self._typing_target_title_color,
        )
        self._ui.show_typing_target(
            typing_target.text_hiragana_alphabet_symbol,
            title='Typing Target (Hiragana)',
            color=self._typing_target_text_color,
            title_color=self._typing_target_title_color,
        )
        self._ui.show_typing_target(
            "".join([target[0] for target in typing_target.typing_target]),
            title='Typing Target (Romaji)',
            color=self._typing_target_text_color,
            title_color=self._typing_target_title_color,
        )

    async def _typing_step(self, typing_target: TypingTargetModel):

        # preparation
        output = OutputModel(
            timestamp=dt.now(),
            typing_target=typing_target.model_copy(deep=True),
            records=[],
        )
        record_queue: queue.Queue = queue.Queue()  # NOTE: it may be redundant.

        # define callbacks
        def on_press_callback(key: KeyCode | Key | None):
            nonlocal typing_target
            nonlocal record_queue

            # preparation
            timestamp = dt.now()
            correct_keys = list(set([x[0] for x in typing_target.typing_target[0] if len(x) > 0]))  # noqa
            pressed_key: str | None = None
            correct: bool = False
            # self._logger.debug(f'correct keys: {correct_keys}')

            # chcek key
            if key == Key.esc:
                _exit()

            elif key == Key.tab:
                _skip()

            elif key == Key.space:
                correct, typing_target.typing_target = self._is_correct(' ', typing_target.typing_target)    # type: ignore  # noqa
                pressed_key = ' '
                self._ui.show_user_input(' ')

            elif isinstance(key, KeyCode) and key in map(KeyCode.from_char, ASCII_CHARS + "¥"):  # noqa
                if key.char is None:
                    raise Exception('key.char is None.')
                correct, typing_target.typing_target = self._is_correct(key.char, typing_target.typing_target)  # noqa
                pressed_key = key.char
                self._ui.show_user_input(key.char, color=EColor.GREEN if correct else EColor.RED)  # noqa

            # record
            if pressed_key is not None:
                record_queue.put(RecordModel(
                    timestamp=timestamp,
                    pressed_key=pressed_key,
                    is_correct=correct,
                    correct_keys=correct_keys,
                ))

            # when done
            if self._is_done(typing_target.typing_target):
                _done()

            # update typing target
            if len(typing_target.typing_target) > 1 and "" in typing_target.typing_target[0]:  # noqa
                # TODO: pop(0) is slow.
                head = typing_target.typing_target.pop(0)
                head.remove("")
                typing_target.typing_target[0].extend(head)

        def on_release_callback(key: KeyCode | Key | None):
            pass

        def _done():
            nonlocal listener  # type: ignore
            self._ui.system_anounce('DONE!', color=self._system_anounce_color)
            listener.stop()
            del listener

        def _skip():
            nonlocal listener
            self._ui.system_anounce('SKIP!', color=self._system_anounce_color)
            listener.stop()
            del listener

        def _exit():
            nonlocal listener  # type: ignore
            listener.stop()
            exit(0)

        # initialize
        output_path = os.path.join(self._record_direc, f'{dt.now().strftime("%Y%m%d_%H%M%S")}.json')  # noqa
        listener = Listener(on_press=on_press_callback, on_release=on_release_callback)  # noqa

        # start
        listener.start()
        listener.join()
        output.records = sorted(list(record_queue.queue), key=lambda x: x.timestamp)  # noqa
        json.dump(output.model_dump(mode='json'), open(output_path, 'a', encoding='utf-8'), indent=4, ensure_ascii=False)  # noqa
        return

    @staticmethod
    def _is_correct(
        char: str,
        typing_target: list[list[str]],
    ) -> tuple[bool, list[list[str]]]:
        '''Check if the input character is correct.

        Args:
            char (str): an input character.
            typing_target (list[list[str]]): typing target.

        Returns:
            bool: True if the input character is correct.
            list[list[str]]: the next typing pattern.
        '''
        # check
        new_typing_target = deepcopy(typing_target)
        new_typing_target[0] = [
            pattern[1:]
            for pattern in new_typing_target[0]
            if pattern.startswith(char)
        ]

        # return result
        if len(new_typing_target[0]) == 0:
            return False, typing_target
        else:
            return True, new_typing_target

    @staticmethod
    def _is_done(typing_target: list[list[str]]) -> bool:
        return (
            len(typing_target) == 0
            or (len(typing_target) == 1 and "" in typing_target[0])
        )
