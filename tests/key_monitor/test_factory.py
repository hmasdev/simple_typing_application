from __future__ import annotations
import pytest

from simple_typing_application.const.key_monitor import EKeyMonitorType  # noqa
from simple_typing_application.models.config_models.key_monitor_config_model import (  # noqa
    BaseKeyMonitorConfigModel,
    SSHKeyboardBasedKeyMonitorConfigModel,
    PynputBasedKeyMonitorConfigModel,
)
from simple_typing_application.key_monitor.sshkeyboard import SSHKeyboardBasedKeyMonitor  # noqa
from simple_typing_application.key_monitor.factory import create_key_monitor, _select_class_and_config_model
from simple_typing_application.key_monitor.pynput import PynputBasedKeyMonitor  # noqa


@pytest.mark.parametrize(
    "key_monitor_type, expected_class, expected_config_model",
    [
        (EKeyMonitorType.PYNPUT, PynputBasedKeyMonitor, PynputBasedKeyMonitorConfigModel),  # noqa
        (EKeyMonitorType.SSHKEYBOARD, SSHKeyboardBasedKeyMonitor, SSHKeyboardBasedKeyMonitorConfigModel),  # noqa
    ],
)
def test_select_class_and_config_model(
    key_monitor_type: EKeyMonitorType,
    expected_class: type,
    expected_config_model: type,
):
    # execute
    key_monitor_cls, key_monitor_config_model = _select_class_and_config_model(key_monitor_type)  # noqa

    # assert
    assert key_monitor_cls is expected_class
    assert key_monitor_config_model is expected_config_model


def test_select_class_and_config_model_raise_value_error():
    # execute
    with pytest.raises(ValueError):
        _select_class_and_config_model("invalid_key_monitor_type")  # type: ignore  # noqa


@pytest.mark.parametrize(
    "key_monitor_type, key_monitor_config, expected_class",
    [
        (
            EKeyMonitorType.PYNPUT,
            PynputBasedKeyMonitorConfigModel(),
            PynputBasedKeyMonitor,
        ),
        (
            EKeyMonitorType.PYNPUT,
            PynputBasedKeyMonitorConfigModel(),
            PynputBasedKeyMonitor,
        ),
        (
            EKeyMonitorType.SSHKEYBOARD,
            SSHKeyboardBasedKeyMonitorConfigModel(),
            SSHKeyboardBasedKeyMonitor,
        ),  # noqa
    ],
)
def test_create_key_monitor(
    key_monitor_type: EKeyMonitorType,
    key_monitor_config: BaseKeyMonitorConfigModel,
    expected_class: type,
):
    # mock
    # for PynputBasedKeyMonitor
    # None

    # execute
    key_monitor = create_key_monitor(
        key_monitor_type,
        key_monitor_config,
    )

    # assert
    assert isinstance(key_monitor, expected_class)


def test_create_key_monitor_raise_import_error(mocker):
    # mock
    mocker.patch(
        "simple_typing_application.key_monitor.factory._select_class_and_config_model",  # noqa
        side_effect=NameError,
    )

    # execute
    with pytest.raises(ImportError):
        create_key_monitor(
            EKeyMonitorType.PYNPUT,
            {},
        )


def test_create_key_monitor_raise_value_error(mocker):
    # mock
    mocker.patch(
        "simple_typing_application.key_monitor.factory._select_class_and_config_model",  # noqa
        side_effect=ValueError,
    )

    # execute
    with pytest.raises(ValueError):
        create_key_monitor(
            "invalid_key_monitor_type",  # type: ignore
            {},
        )
