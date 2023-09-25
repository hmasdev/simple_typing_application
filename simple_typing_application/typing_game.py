import asyncio
from datetime import datetime as dt
import json
from logging import getLogger, Logger
import os


from .const.color import EColor
from .const.keys import EMetaKey
from .key_monitor.base import BaseKeyMonitor
from .models.output_model import OutputModel
from .models.record_model import RecordModel
from .models.typing_target_model import TypingTargetModel
from .sentence_generator.base import BaseSentenceGenerator
from .ui.base import BaseUserInterface


def _input_char_is_correct(
    char: str,
    typing_target: TypingTargetModel,
) -> tuple[bool, TypingTargetModel]:
    '''Check if the input character is correct.

    Args:
        char (str): an input character.
        typing_target (TypingTargetModel): typing target.

    Returns:
        bool: True if the input character is correct.
        TypingTargetModel: the next typing pattern.
    '''
    # check
    new_typing_target = typing_target.model_copy(deep=True)
    new_typing_target.typing_target[0] = [
        pattern[1:]
        for pattern in new_typing_target.typing_target[0]
        if pattern.startswith(char)
    ]

    # return result
    if len(new_typing_target.typing_target[0]) == 0:
        return False, typing_target
    else:
        if "" in new_typing_target.typing_target[0]:
            # NOTE: When '' in typing_target.typing_target[0], it means that a patten has been input correctly.  # noqa
            # TODO: pop(0) is slow.
            head = new_typing_target.typing_target.pop(0)
            head.remove("")

            if new_typing_target.typing_target:
                new_typing_target.typing_target[0].extend(head)

        return True, new_typing_target


def _typing_is_done(typing_target: TypingTargetModel) -> bool:
    '''Check if typing is done.

    Args:
        typing_target (TypingTargetModel): typing target.

    Returns:
        bool: True if typing is done.

    NOTE:
        Typing is done when typing_target.typing_target is empty.
    '''  # noqa
    return len(typing_target.typing_target) == 0


class TypingGame:

    _typing_target_title_color = EColor.YELLOW
    _typing_target_text_color = EColor.DEFAULT
    _correct_user_input_color = EColor.GREEN
    _incorrect_user_input_color = EColor.RED
    _system_anounce_color = EColor.YELLOW

    def __init__(
        self,
        sentence_generator: BaseSentenceGenerator,
        key_monitor: BaseKeyMonitor,
        ui: BaseUserInterface,
        record_direc: str,
        logger: Logger = getLogger(__name__),
    ):
        self._sentence_generator = sentence_generator
        self._key_monitor = key_monitor
        self._ui = ui
        self._record_direc = record_direc
        self._logger = logger

        self.__current_typing_target: TypingTargetModel | None = None
        self.__current_records: list[RecordModel] | None = None

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

        # initialize
        self.__initialize_typing_step(typing_target.model_copy(deep=True))
        assert self.__current_typing_target is not None
        assert self.__current_records is not None
        output = OutputModel(
            timestamp=dt.now(),
            typing_target=typing_target.model_copy(deep=True),
            records=self.__current_records,
        )
        output_path = os.path.join(self._record_direc, f'{dt.now().strftime("%Y%m%d_%H%M%S")}.json')  # noqa

        # start
        self._key_monitor.start()

        # wait for done
        # post process
        output.records = sorted(list(self.__current_records), key=lambda x: x.timestamp)  # noqa
        self._logger.debug(f'The following data has been saved to {output_path}: {output.model_dump(mode="json")}')  # noqa
        json.dump(output.model_dump(mode='json'), open(output_path, 'a', encoding='utf-8'), indent=4, ensure_ascii=False)  # noqa

        # clean up
        self.__clean_up_typing_step()

        return

    def __initialize_typing_step(self, typing_target: TypingTargetModel):
        self.__current_typing_target = typing_target
        self.__current_records = []
        self._key_monitor.set_on_press_callback(self.__on_press_callback)
        self._key_monitor.set_on_release_callback(self.__on_release_callback)

    def __clean_up_typing_step(self):
        self.__current_typing_target = None
        self.__current_records = None
        self._key_monitor.set_on_press_callback(None)
        self._key_monitor.set_on_release_callback(None)

    def __skip_typing_step(self):
        self._ui.system_anounce('SKIP!', color=self._system_anounce_color)
        self._key_monitor.stop()

    def __done_typing_step(self):
        self._ui.system_anounce('DONE!', color=self._system_anounce_color)
        self._key_monitor.stop()

    def __exit_typing_step(self):
        self._ui.system_anounce('EXIT!', color=self._system_anounce_color)
        self._key_monitor.stop()
        exit(-1)

    def __on_press_callback(
        self,
        key: EMetaKey | str | None,
    ) -> bool | None:
        # validation
        assert self.__current_typing_target is not None
        assert self.__current_records is not None

        # preparation
        record = RecordModel(
            timestamp=dt.now(),
            pressed_key='',
            is_correct=False,
            correct_keys=list(set([x[0] for x in self.__current_typing_target.typing_target[0] if len(x) > 0])),  # noqa
        )
        self._logger.debug(f'current typing target: {self.__current_typing_target}')  # noqa
        self._logger.debug(f'correct keys: {record.correct_keys}')

        # chcek key
        if key == EMetaKey.ESC:
            self._logger.debug('Escape key has been pressed.')
        elif key == EMetaKey.TAB:
            self._logger.debug('Tab key has been pressed.')
        elif isinstance(key, str):
            self._logger.debug(f'{key} key has been pressed.')
            record.pressed_key = key
            record.is_correct, self.__current_typing_target = _input_char_is_correct(key, self.__current_typing_target)  # noqa
            self._ui.show_user_input(key, color=EColor.GREEN if record.is_correct else EColor.RED)  # noqa
        else:
            self._logger.debug('key is invalid.')

        # record
        if record.pressed_key != '':
            self.__current_records.append(record)

        return None

    def __on_release_callback(self, key: EMetaKey | str | None) -> bool | None:
        self._logger.debug(f'{key} key has been released.')

        # validation
        assert self.__current_typing_target is not None
        assert self.__current_records is not None

        # meta key
        if key == EMetaKey.ESC:
            self.__exit_typing_step()
            return False
        elif key == EMetaKey.TAB:
            self.__skip_typing_step()
            return False

        # check if typing is done
        if _typing_is_done(self.__current_typing_target):
            self._logger.debug('Typing is done.')
            self.__done_typing_step()
            return False

        return None
