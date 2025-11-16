from __future__ import annotations
import asyncio
from datetime import datetime as dt
import logging
from unittest import mock
import pytest
from simple_typing_application.const.keys import EMetaKey
from simple_typing_application.models.output_model import OutputModel
from simple_typing_application.models.record_model import RecordModel
from simple_typing_application.models.typing_target_model import TypingTargetModel  # noqa
from simple_typing_application.key_monitor.base import BaseKeyMonitor
from simple_typing_application.sentence_generator.base import BaseSentenceGenerator  # noqa
from simple_typing_application.typing_game import (
    _input_char_is_correct,
    _typing_is_done,
    TypingGame,
)
from simple_typing_application.ui.base import BaseUserInterface


FIXED_TIMESTAMP: dt = dt(2021, 1, 1, 0, 0, 0, 0)


@pytest.fixture(scope="function")
def typing_game_with_mocks(mocker) -> tuple[TypingGame, dict[str, mock.MagicMock]]:  # type: ignore # noqa
    # create mocks
    mocks = dict(
        mock_key_monitor=mocker.MagicMock(spec=BaseKeyMonitor),
        mock_sentence_generator=mocker.MagicMock(spec=BaseSentenceGenerator),
        mock_user_interface=mocker.MagicMock(spec=BaseUserInterface),
        mock_os_make_dirs=mocker.patch("simple_typing_application.typing_game.os.makedirs"),  # noqa
        mock_dt=mocker.patch("simple_typing_application.typing_game.dt"),
        mock_exit=mocker.patch("builtins.exit"),
        mock_record_direc="./dummy",
        mock_open=mocker.patch("builtins.open", mocker.mock_open(read_data="")),  # noqa
        mock_json_dump=mocker.patch("simple_typing_application.typing_game.json.dump"),  # noqa
    )
    mocks["mock_dt"].now = mocker.Mock(return_value=FIXED_TIMESTAMP)

    # create typing game
    typing_game = TypingGame(
        sentence_generator=mocks["mock_sentence_generator"],
        key_monitor=mocks["mock_key_monitor"],
        ui=mocks["mock_user_interface"],
        record_direc=mocks["mock_record_direc"],
    )

    yield typing_game, mocks


@pytest.mark.parametrize(
    "char, typing_target, expected",
    [
        # Alphabet Cases (True)
        (
            "a",
            TypingTargetModel(
                text="abc",  # dummy
                text_hiragana_alphabet_symbol="abc",  # dummy
                typing_target=[["a"], ["b"], ["c"]],
            ),
            (
                True,
                TypingTargetModel(
                    text="abc",  # dummy
                    text_hiragana_alphabet_symbol="abc",  # dummy
                    typing_target=[["b"], ["c"]],
                ),
            ),
        ),
        # Alphabet Cases (Single, True)
        (
            "a",
            TypingTargetModel(
                text="a",  # dummy
                text_hiragana_alphabet_symbol="a",  # dummy
                typing_target=[["a"]],
            ),
            (
                True,
                TypingTargetModel(
                    text="a",  # dummy
                    text_hiragana_alphabet_symbol="a",  # dummy
                    typing_target=[],
                ),
            ),
        ),
        # Alphabet Cases (False)
        (
            "z",
            TypingTargetModel(
                text="abc",  # dummy
                text_hiragana_alphabet_symbol="abc",  # dummy
                typing_target=[["a"], ["b"], ["c"]],
            ),
            (
                False,
                TypingTargetModel(
                    text="abc",  # dummy
                    text_hiragana_alphabet_symbol="abc",  # dummy
                    typing_target=[["a"], ["b"], ["c"]],
                ),
            ),
        ),
        # Hiragana Cases (True 1)
        (
            "t",
            TypingTargetModel(
                text="ち",  # dummy
                text_hiragana_alphabet_symbol="ち",  # dummy
                typing_target=[["ti", "chi"]],
            ),
            (
                True,
                TypingTargetModel(
                    text="ち",  # dummy
                    text_hiragana_alphabet_symbol="ち",  # dummy
                    typing_target=[["i"]],
                ),
            ),
        ),
        # Hiragana Cases (True 2)
        (
            "c",
            TypingTargetModel(
                text="ち",  # dummy
                text_hiragana_alphabet_symbol="ち",  # dummy
                typing_target=[["ti", "chi"]],
            ),
            (
                True,
                TypingTargetModel(
                    text="ち",  # dummy
                    text_hiragana_alphabet_symbol="ち",  # dummy
                    typing_target=[["hi"]],
                ),
            ),
        ),
        # Hiragana Cases (False)
        (
            "x",
            TypingTargetModel(
                text="ち",  # dummy
                text_hiragana_alphabet_symbol="ち",  # dummy
                typing_target=[["ti", "chi"]],
            ),
            (
                False,
                TypingTargetModel(
                    text="ち",  # dummy
                    text_hiragana_alphabet_symbol="ち",  # dummy
                    typing_target=[["ti", "chi"]],
                ),
            ),
        ),
    ],
)
def test_input_char_is_correct(
    char: str,
    typing_target: TypingTargetModel,
    expected: tuple[bool, TypingTargetModel],
):
    # execute
    actual = _input_char_is_correct(char, typing_target)
    assert actual == expected


@pytest.mark.parametrize(
    "typing_target, expected",
    [
        (
            TypingTargetModel(
                text="abc",  # dummy
                text_hiragana_alphabet_symbol="abc",  # dummy
                typing_target=[],
            ),
            True,
        ),
        (
            TypingTargetModel(
                text="abc",  # dummy
                text_hiragana_alphabet_symbol="abc",  # dummy
                typing_target=[["c"]],
            ),
            False,
        ),
    ],
)
def test_typing_is_done(
    typing_target: TypingTargetModel,
    expected: bool,
):
    # execute
    actual = _typing_is_done(typing_target)
    assert actual == expected


def test_typing_game_instantiation(typing_game_with_mocks: tuple[TypingGame, dict[str, mock.MagicMock]]):  # type: ignore # noqa
    # unpack
    typing_game, mocks = typing_game_with_mocks

    # assert
    assert typing_game._sentence_generator is mocks["mock_sentence_generator"]
    assert typing_game._key_monitor is mocks["mock_key_monitor"]
    assert typing_game._ui is mocks["mock_user_interface"]
    assert typing_game._record_direc == mocks["mock_record_direc"]
    mocks["mock_os_make_dirs"].assert_called_once_with(mocks["mock_record_direc"], exist_ok=True)  # noqa


def test_typing_game__show_typing_target(typing_game_with_mocks: tuple[TypingGame, dict[str, mock.MagicMock]]):  # noqa
    # unpack
    typing_game, mocks = typing_game_with_mocks

    # preparation
    typing_target = TypingTargetModel(
        text="abc",
        text_hiragana_alphabet_symbol="abc",
        typing_target=[["a"], ["b"], ["c"]],
    )

    # execute
    typing_game._show_typing_target(typing_target)

    # assert
    mocks["mock_user_interface"].show_typing_target.assert_any_call(
        typing_target.text,
        title="Typing Target",
        color=typing_game._typing_target_text_color,
        title_color=typing_game._typing_target_title_color,
    )
    mocks["mock_user_interface"].show_typing_target.assert_any_call(
        typing_target.text_hiragana_alphabet_symbol,
        title="Typing Target (Hiragana)",
        color=typing_game._typing_target_text_color,
        title_color=typing_game._typing_target_title_color,
    )
    mocks["mock_user_interface"].show_typing_target.assert_any_call(
        "".join([target[0] for target in typing_target.typing_target]),
        title="Typing Target (Romaji)",
        color=typing_game._typing_target_text_color,
        title_color=typing_game._typing_target_title_color,
    )


def test_typing_game___initialize_typing_step(typing_game_with_mocks: tuple[TypingGame, dict[str, mock.MagicMock]]):  # noqa
    # unpack
    typing_game, mocks = typing_game_with_mocks

    # preparation
    typing_target = TypingTargetModel(
        text="abc",
        text_hiragana_alphabet_symbol="abc",
        typing_target=[["a"], ["b"], ["c"]],
    )

    # execute
    typing_game._TypingGame__initialize_typing_step(typing_target)  # type: ignore  # noqa

    # assert
    assert typing_game._TypingGame__current_typing_target is typing_target  # type: ignore  # noqa
    assert typing_game._TypingGame__current_records == []  # type: ignore
    typing_game._key_monitor.set_on_press_callback.assert_called_once_with(typing_game._TypingGame__on_press_callback)  # type: ignore # noqa

    on_release_callback_of_typing_game = typing_game._TypingGame__on_release_callback  # type: ignore # noqa
    typing_game._key_monitor.set_on_release_callback.assert_called_once_with(on_release_callback_of_typing_game)  # type: ignore # noqa


def test_typing_game___clean_up_typing_step(typing_game_with_mocks: tuple[TypingGame, dict[str, mock.MagicMock]]):  # noqa
    # unpack
    typing_game, mocks = typing_game_with_mocks

    # preparation
    typing_target = TypingTargetModel(
        text="abc",
        text_hiragana_alphabet_symbol="abc",
        typing_target=[["a"], ["b"], ["c"]],
    )
    typing_game._TypingGame__initialize_typing_step(typing_target)  # type: ignore  # noqa
    typing_game._key_monitor.set_on_press_callback.reset_mock()  # type: ignore  # noqa
    typing_game._key_monitor.set_on_release_callback.reset_mock()  # type: ignore  # noqa

    # execute
    typing_game._TypingGame__clean_up_typing_step()  # type: ignore

    # assert
    assert typing_game._TypingGame__current_typing_target is None  # type: ignore  # noqa
    assert typing_game._TypingGame__current_records is None  # type: ignore  # noqa
    typing_game._key_monitor.set_on_press_callback.assert_called_once_with(None)  # type: ignore # noqa
    typing_game._key_monitor.set_on_release_callback.assert_called_once_with(None)  # type: ignore # noqa


def test_typing_game__skip_typing_step(typing_game_with_mocks: tuple[TypingGame, dict[str, mock.MagicMock]]):  # noqa
    # unpack
    typing_game, _ = typing_game_with_mocks

    # execute
    typing_game._ui.system_anounce.reset_mock()  # type: ignore  # noqa
    typing_game._TypingGame__skip_typing_step()  # type: ignore

    # assert
    typing_game._ui.system_anounce.assert_called_once_with(  # type: ignore  # noqa
        "SKIP!",
        color=typing_game._system_anounce_color,
    )
    typing_game._key_monitor.stop.assert_called_once_with()  # type: ignore  # noqa


def test_typing_game__done_typing_step(typing_game_with_mocks: tuple[TypingGame, dict[str, mock.MagicMock]]):  # noqa
    # unpack
    typing_game, _ = typing_game_with_mocks

    # execute
    typing_game._ui.system_anounce.reset_mock()  # type: ignore  # noqa
    typing_game._TypingGame__done_typing_step()  # type: ignore

    # assert
    typing_game._ui.system_anounce.assert_called_once_with(  # type: ignore  # noqa
        "DONE!",
        color=typing_game._system_anounce_color,
    )
    typing_game._key_monitor.stop.assert_called_once_with()  # type: ignore  # noqa


def test_typing_game__exit_typing_step(typing_game_with_mocks: tuple[TypingGame, dict[str, mock.MagicMock]]):  # noqa
    # unpack
    typing_game, mocks = typing_game_with_mocks

    # execute
    typing_game._ui.system_anounce.reset_mock()  # type: ignore  # noqa
    typing_game._TypingGame__exit_typing_step()  # type: ignore

    # assert
    typing_game._ui.system_anounce.assert_called_once_with(  # type: ignore
        "EXIT!",
        color=typing_game._system_anounce_color,
    )
    typing_game._key_monitor.stop.assert_called_once_with()  # type: ignore
    mocks["mock_exit"].assert_called_once_with(-1)


@pytest.mark.parametrize(
    "key,typing_target,expected___current_typing_target,expected____current_records,expected",  # noqa
    [
        (
            "a",
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["a"], ["b"], ["c"]],
            ),
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["b"], ["c"]],
            ),
            [
                RecordModel(
                    timestamp=FIXED_TIMESTAMP,
                    pressed_key="a",
                    is_correct=True,
                    correct_keys=["a"],
                ),
            ],
            None,
        ),
        (
            "z",
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["a"], ["b"], ["c"]],
            ),
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["a"], ["b"], ["c"]],
            ),
            [
                RecordModel(
                    timestamp=FIXED_TIMESTAMP,
                    pressed_key="z",
                    is_correct=False,
                    correct_keys=["a"],
                ),
            ],
            None,
        ),
        (
            EMetaKey.ESC,
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["a"], ["b"], ["c"]],
            ),
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["a"], ["b"], ["c"]],
            ),
            [],
            None,
        ),
        (
            EMetaKey.TAB,
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["a"], ["b"], ["c"]],
            ),
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["a"], ["b"], ["c"]],
            ),
            [],
            None,
        ),
        (
            None,
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["a"], ["b"], ["c"]],
            ),
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["a"], ["b"], ["c"]],
            ),
            [],
            None,
        ),
    ],
)
def test_typing_game__on_press_callback(
    key: EMetaKey | str | None,
    typing_target: TypingTargetModel,
    expected___current_typing_target: TypingTargetModel,
    expected____current_records: list[RecordModel],
    expected: bool | None,
    typing_game_with_mocks: tuple[TypingGame, dict[str, mock.MagicMock]],
):
    # unpack
    typing_game, mocks = typing_game_with_mocks

    # execute
    typing_game._TypingGame__initialize_typing_step(typing_target)  # type: ignore  # noqa
    actual = typing_game._TypingGame__on_press_callback(key)  # type: ignore

    # assert
    assert typing_game._TypingGame__current_typing_target == expected___current_typing_target  # type: ignore  # noqa
    assert typing_game._TypingGame__current_records == expected____current_records  # type: ignore  # noqa
    assert actual == expected


@pytest.mark.parametrize(
    "key, current_typing_target, expected",
    [
        (
            EMetaKey.ESC,
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["a"], ["b"], ["c"]],
            ),
            False,
        ),
        (
            EMetaKey.TAB,
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["a"], ["b"], ["c"]],
            ),
            False,
        ),
        (
            EMetaKey.ESC,
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[],
            ),
            False,
        ),
        (
            EMetaKey.TAB,
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[],
            ),
            False,
        ),
        (
            None,
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["a"], ["b"], ["c"]],
            ),
            None,
        ),
        (
            "a",
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["a"], ["b"], ["c"]],
            ),
            None,
        ),
        (
            None,
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[],
            ),
            False,
        ),
        (
            "a",
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[],
            ),
            False,
        ),
    ],
)
def test_typing_game__on_release_callback(
    key: EMetaKey | str | None,
    current_typing_target: TypingTargetModel,
    expected: bool | None,
    typing_game_with_mocks: tuple[TypingGame, dict[str, mock.MagicMock]],
):
    # unpack
    typing_game, mocks = typing_game_with_mocks

    # execute
    typing_game._TypingGame__initialize_typing_step(current_typing_target)  # type: ignore  # noqa
    actual = typing_game._TypingGame__on_release_callback(key)  # type: ignore

    # assert
    assert actual == expected


@pytest.mark.parametrize(
    "typing_target, expected_output",
    [
        (
            TypingTargetModel(
                text="abc",
                text_hiragana_alphabet_symbol="abc",
                typing_target=[["a"], ["b"], ["c"]],
            ),
            OutputModel(
                timestamp=FIXED_TIMESTAMP,
                typing_target=TypingTargetModel(
                    text="abc",
                    text_hiragana_alphabet_symbol="abc",
                    typing_target=[["a"], ["b"], ["c"]],
                ),
                records=[
                    # NOTE: `sorted` is stable sort.
                    # See https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts  # noqa
                    RecordModel(
                        timestamp=FIXED_TIMESTAMP,
                        pressed_key="a",
                        is_correct=True,
                        correct_keys=["a"],
                    ),
                    RecordModel(
                        timestamp=FIXED_TIMESTAMP,
                        pressed_key="b",
                        is_correct=True,
                        correct_keys=["b"],
                    ),
                    RecordModel(
                        timestamp=FIXED_TIMESTAMP,
                        pressed_key="z",
                        is_correct=False,
                        correct_keys=["c"],
                    ),
                    RecordModel(
                        timestamp=FIXED_TIMESTAMP,
                        pressed_key="c",
                        is_correct=True,
                        correct_keys=["c"],
                    ),
                ],
            ),
        )
    ],
)
def test_typing_game__typing_step(
    typing_target: TypingTargetModel,
    expected_output: OutputModel,
    typing_game_with_mocks: tuple[TypingGame, dict[str, mock.MagicMock]],
    mocker,
):
    # unpack
    typing_game, mocks = typing_game_with_mocks
    assert typing_game._TypingGame__current_typing_target is None  # type: ignore  # noqa
    assert typing_game._TypingGame__current_records is None  # type: ignore  # noqa

    # preparation
    def emulate_pressing_keys():
        nonlocal typing_game  # noqa
        nonlocal expected_output  # noqa
        # emulate pressing keys
        for record in expected_output.records:
            typing_game._TypingGame__on_press_callback(record.pressed_key)  # type: ignore  # noqa
            typing_game._TypingGame__on_release_callback(record.pressed_key)  # type: ignore  # noqa
            logging.debug(f"current records: {typing_game._TypingGame__current_records}")  # type: ignore  # noqa

    mocks["mock_key_monitor"].start = mocker.Mock(side_effect=emulate_pressing_keys)  # type: ignore  # noqa

    # execute
    asyncio.run(typing_game._typing_step(typing_target))

    # assert
    typing_game._key_monitor.start.assert_called_once_with()  # type: ignore  # noqa
    mocks["mock_json_dump"].assert_called_once_with(
        expected_output.model_dump(mode="json"), mocks["mock_open"].return_value, indent=4, ensure_ascii=False
    )
