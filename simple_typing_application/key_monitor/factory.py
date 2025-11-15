from __future__ import annotations
from logging import getLogger, Logger


from .base import BaseKeyMonitor
from .pynput import PynputBasedKeyMonitor
from .sshkeyboard import SSHKeyboardBasedKeyMonitor
from ..const.key_monitor import EKeyMonitorType
from ..models.config_models.key_monitor_config_model import (
    SSHKeyboardBasedKeyMonitorConfigModel,
    BaseKeyMonitorConfigModel,
    PynputBasedKeyMonitorConfigModel,
)


def _select_class_and_config_model(key_monitor_type: EKeyMonitorType) -> tuple[type, type]:  # noqa
    if key_monitor_type == EKeyMonitorType.PYNPUT:
        return PynputBasedKeyMonitor, PynputBasedKeyMonitorConfigModel
    elif key_monitor_type == EKeyMonitorType.SSHKEYBOARD:
        return SSHKeyboardBasedKeyMonitor, SSHKeyboardBasedKeyMonitorConfigModel  # noqa
    else:
        raise ValueError(f"Unsupported key monitor type: {key_monitor_type}")


def create_key_monitor(
    key_monitor_type: EKeyMonitorType,
    dict_config: dict[str, str | float | int | bool | None | dict | list],
    logger: Logger = getLogger(__name__),
) -> BaseKeyMonitor:
    # select key monitor class and config model
    try:
        key_monitor_cls, key_monitor_config_model = _select_class_and_config_model(key_monitor_type)  # noqa
    except NameError:
        raise ImportError(
            f"Failed to import key monitor class and config model for key_monitor_type={key_monitor_type}"
        )  # noqa

    # create key monitor
    logger.debug(f"create {key_monitor_cls.__name__}")
    key_monitor_config: BaseKeyMonitorConfigModel = key_monitor_config_model(**dict_config)  # noqa
    key_monitor: BaseKeyMonitor = key_monitor_cls(**key_monitor_config.model_dump())  # type: ignore # noqa

    return key_monitor
