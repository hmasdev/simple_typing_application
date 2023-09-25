import pytest

from simple_typing_application.const.key_monitor import EKeyMonitorType  # noqa
from simple_typing_application.models.config_models.key_monitor_config_model import (  # noqa
    BaseKeyMonitorConfigModel,
    PynputBasedKeyMonitorConfigModel,
)
from simple_typing_application.key_monitor.factory import create_key_monitor  # noqa
from simple_typing_application.key_monitor.pynput import PynputBasedKeyMonitor  # noqa


@pytest.mark.parametrize(
    "key_monitor_type, key_monitor_config_dict, expected_class",
    [
        (
            EKeyMonitorType.PYNPUT,
            PynputBasedKeyMonitorConfigModel().model_dump(),
            PynputBasedKeyMonitor,
        ),
        (
            EKeyMonitorType.PYNPUT,
            {},
            PynputBasedKeyMonitor,
        )
    ]
)
def test_create_key_monitor(
    key_monitor_type: EKeyMonitorType,
    key_monitor_config_dict: dict[str, str | float | int | bool | None | dict | list],  # noqa
    expected_class: type,
    mocker,
):

    # mock
    # for PynputBasedKeyMonitor
    # None

    # execute
    key_monitor = create_key_monitor(
        key_monitor_type,
        key_monitor_config_dict,
    )

    # assert
    assert isinstance(key_monitor, expected_class)
