from pynput import keyboard
import pytest
from simple_typing_application.const.keys import EMetaKey
from simple_typing_application.key_monitor.base import BaseKeyMonitor
from simple_typing_application.key_monitor.pynput import PynputBasedKeyMonitor


PYNPUT_KEY_MAP: tuple[tuple[keyboard.Key | keyboard.KeyCode | None, EMetaKey | str | None], ...] = (  # noqa
    (keyboard.Key.esc, EMetaKey.ESC),
    (keyboard.Key.tab, EMetaKey.TAB),
    (keyboard.Key.space, ' '),
    (keyboard.Key.ctrl, None),
    (keyboard.Key.alt, None),
    (keyboard.Key.cmd, None),
    (keyboard.Key.caps_lock, None),
    (keyboard.Key.shift, None),
    (keyboard.Key.backspace, None),
    (keyboard.Key.enter, None),
    (keyboard.Key.delete, None),
    (keyboard.Key.up, None),
    (keyboard.Key.down, None),
    (keyboard.Key.left, None),
    (keyboard.Key.right, None),
    (keyboard.Key.home, None),
    (keyboard.Key.end, None),
    (keyboard.Key.page_up, None),
    (keyboard.Key.page_down, None),
    (keyboard.Key.insert, None),
    (keyboard.KeyCode.from_char('a'), 'a'),
    (keyboard.KeyCode.from_char('A'), 'A'),
    (keyboard.KeyCode.from_char('#'), '#'),
    (None, None),
)


def test_inheritance():
    assert issubclass(PynputBasedKeyMonitor, BaseKeyMonitor)


@pytest.mark.parametrize(
    "key, expected",
    list(PYNPUT_KEY_MAP),
)
def test__clean_key(
    key: keyboard.Key | keyboard.KeyCode | None,
    expected: EMetaKey | str | None,
):
    # execute
    actual = PynputBasedKeyMonitor()._clean_key(key)
    # assert
    assert actual == expected


@pytest.mark.parametrize(
    "key, intemediate_expected",
    list(PYNPUT_KEY_MAP),
)
def test__on_press_callback_wrapper(
    key: keyboard.Key | keyboard.KeyCode,
    intemediate_expected: EMetaKey | str | None,
    mocker
):

    # mock
    mock_callback = mocker.MagicMock()

    # preparation
    key_monitor = PynputBasedKeyMonitor()
    key_monitor.set_on_press_callback(mock_callback)

    # execute
    key_monitor._on_press_callback_wrapper(key)

    # assert
    mock_callback.assert_called_once_with(intemediate_expected)


@pytest.mark.parametrize(
    "key, intemediate_expected",
    list(PYNPUT_KEY_MAP),
)
def test__on_release_callback_wrapper(
    key: keyboard.Key | keyboard.KeyCode,
    intemediate_expected: EMetaKey | str | None,
    mocker
):

    # mock
    mock_callback = mocker.MagicMock()

    # preparation
    key_monitor = PynputBasedKeyMonitor()
    key_monitor.set_on_release_callback(mock_callback)

    # execute
    key_monitor._on_release_callback_wrapper(key)

    # assert
    mock_callback.assert_called_once_with(intemediate_expected)


def test_start(mocker):

    # mock
    mock_keyboard_listener = mocker.MagicMock(spec=keyboard.Listener)
    mocker.patch(
        'simple_typing_application.key_monitor.pynput.keyboard.Listener',
        return_value=mock_keyboard_listener
    )

    # preparation
    key_monitor = PynputBasedKeyMonitor()

    # execute
    key_monitor.start()

    # assert
    mock_keyboard_listener.start.assert_called_once()
    mock_keyboard_listener.join.assert_called_once()


def test_stop(mocker):

    # mock
    mock_keyboard_listener = mocker.MagicMock(spec=keyboard.Listener)
    mocker.patch(
        'simple_typing_application.key_monitor.pynput.keyboard.Listener',
        return_value=mock_keyboard_listener
    )

    # preparation
    key_monitor = PynputBasedKeyMonitor()

    # execute
    key_monitor.start()
    mock_keyboard_listener.stop.assert_not_called()
    key_monitor.stop()

    # assert
    mock_keyboard_listener.stop.assert_called_once()
    assert key_monitor._listener is None


def test_stop_before_start(mocker, caplog):

    # mock
    mock_keyboard_listener = mocker.MagicMock(spec=keyboard.Listener)
    mocker.patch(
        'simple_typing_application.key_monitor.pynput.keyboard.Listener',
        return_value=mock_keyboard_listener
    )

    # preparation
    key_monitor = PynputBasedKeyMonitor()

    # execute
    key_monitor.stop()

    # assert
    # Test whether the warning message is output.
    caplog.records[0].message == f'{key_monitor.__class__.__name__}() has not been started.'  # noqa
    caplog.records[0].levelname == 'WARNING'
