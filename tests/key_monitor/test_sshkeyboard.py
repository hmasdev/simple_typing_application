from __future__ import annotations
from threading import Thread
import pytest
from sshkeyboard import stop_listening
from simple_typing_application.const.keys import EMetaKey
from simple_typing_application.key_monitor.sshkeyboard import SSHKeyboardBasedKeyMonitor  # noqa
from simple_typing_application.key_monitor.base import BaseKeyMonitor


KEY_STR_MAP: tuple[tuple[str, EMetaKey | str | None], ...] = (  # noqa
    ("esc", EMetaKey.ESC),
    ("backspace", None),
    ("insert", None),
    ("delete", None),
    ("pageup", None),
    ("pagedown", None),
    ("home", None),
    ("end", None),
    ("up", None),
    ("down", None),
    ("right", None),
    ("left", None),
    ("f1", None),
    ("f2", None),
    ("f3", None),
    ("f4", None),
    ("f5", None),
    ("f6", None),
    ("f7", None),
    ("f8", None),
    ("f9", None),
    ("f10", None),
    ("f11", None),
    ("f12", None),
    ("f13", None),
    ("f14", None),
    ("f15", None),
    ("f16", None),
    ("f17", None),
    ("f18", None),
    ("f19", None),
    ("f20", None),
    ("enter", None),
    ("space", " "),
    ("tab", EMetaKey.TAB),
    ('a', 'a'),
    ('A', 'A'),
    ('#', '#'),
)


def test_inheritance():
    assert issubclass(SSHKeyboardBasedKeyMonitor, BaseKeyMonitor)


def test__reset_keys_queue():
    # preparation
    key_monitor = SSHKeyboardBasedKeyMonitor()
    key_monitor._SSHKeyboardBasedKeyMonitor__keys_queue.append('a')  # type: ignore  # noqa
    assert len(key_monitor._SSHKeyboardBasedKeyMonitor__keys_queue) > 0   # type: ignore  # noqa

    # execute
    key_monitor._reset_keys_queue()

    # assert
    assert len(key_monitor._SSHKeyboardBasedKeyMonitor__keys_queue) == 0   # type: ignore  # noqa


@pytest.mark.parametrize(
    "key, expected",
    list(KEY_STR_MAP),
)
def test__clean_key(
    key: str,
    expected: EMetaKey | str | None,
):
    # execute
    actual = SSHKeyboardBasedKeyMonitor()._clean_key(key)
    # assert
    assert actual == expected


@pytest.mark.parametrize(
    "key, intemediate_expected",
    list(KEY_STR_MAP),
)
def test__on_press_callback_wrapper(
    key: str,
    intemediate_expected: EMetaKey | str | None,
    mocker
):

    # mock
    mock_callback = mocker.MagicMock()

    # preparation
    key_monitor = SSHKeyboardBasedKeyMonitor()
    key_monitor.set_on_press_callback(mock_callback)

    # execute
    key_monitor._on_press_callback_wrapper(key)

    # assert
    mock_callback.assert_called_once_with(intemediate_expected)


@pytest.mark.parametrize(
    "key, intemediate_expected",
    list(KEY_STR_MAP),
)
def test__on_release_callback_wrapper(
    key: str,
    intemediate_expected: EMetaKey | str | None,
    mocker
):

    # mock
    mock_callback = mocker.MagicMock()

    # preparation
    key_monitor = SSHKeyboardBasedKeyMonitor()
    key_monitor.set_on_release_callback(mock_callback)

    # execute
    key_monitor._on_release_callback_wrapper(key)

    # assert
    mock_callback.assert_called_once_with(intemediate_expected)


def test_start(mocker):

    # mock
    mock_thread = mocker.MagicMock(spec=Thread)
    mock_Thread = mocker.patch(
        'simple_typing_application.key_monitor.sshkeyboard.Thread',
        return_value=mock_thread,
    )
    mock_listen_keyboard = mocker.patch(
        'simple_typing_application.key_monitor.sshkeyboard.listen_keyboard',
    )

    # preparation
    key_monitor = SSHKeyboardBasedKeyMonitor()

    # execute
    key_monitor.start()

    # assert
    mock_Thread.assert_called_once_with(
        target=mock_listen_keyboard,
        kwargs=dict(
            on_press=key_monitor._on_press_callback_wrapper,
            on_release=key_monitor._on_release_callback_wrapper,
        )
    )
    mock_thread.start.assert_called_once()
    mock_thread.join.assert_called_once()


def test_stop(mocker):
    # TODO: fix this test

    # mock
    mock_thread = mocker.MagicMock(spec=Thread)
    mock_Thread = mocker.patch(
        'simple_typing_application.key_monitor.sshkeyboard.Thread',
        return_value=mock_thread,
    )
    mock_listen_keyboard = mocker.patch(
        'simple_typing_application.key_monitor.sshkeyboard.listen_keyboard',
    )
    mock_stop_listening = mocker.patch(
        'simple_typing_application.key_monitor.sshkeyboard.stop_listening',
        side_effect=stop_listening
    )

    # preparation
    key_monitor = SSHKeyboardBasedKeyMonitor()

    # execute
    key_monitor.start()
    # emulate send 'a' key
    key_monitor._SSHKeyboardBasedKeyMonitor__keys_queue.append('a')  # type: ignore  # noqa
    mock_stop_listening.assert_not_called()
    key_monitor.stop()

    # assert
    mock_Thread.assert_called_once_with(
        target=mock_listen_keyboard,
        kwargs=dict(
            on_press=key_monitor._on_press_callback_wrapper,
            on_release=key_monitor._on_release_callback_wrapper,
        )
    )
    mock_thread.start.assert_called_once()
    mock_thread.join.assert_called_once()
    assert len(key_monitor._SSHKeyboardBasedKeyMonitor__keys_queue) == 0  # type: ignore  # noqa
    mock_stop_listening.assert_called_once()
