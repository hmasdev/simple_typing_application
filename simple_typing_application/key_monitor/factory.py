from logging import getLogger, Logger


from .base import BaseKeyMonitor
from .pynput import PynputBasedKeyMonitor
from ..const.key_monitor import EKeyMonitorType
from ..models.config_models.key_monitor_config_model import (
    BaseKeyMonitorConfigModel,
    PynputBasedKeyMonitorConfigModel,
)


def create_key_monitor(
    key_monitor_type: EKeyMonitorType,
    dict_config: dict[str, str | float | int | bool | None | dict | list],
    logger: Logger = getLogger(__name__),
) -> BaseKeyMonitor:

    # select key monitor class and config model
    try:
        key_monitor_cls = {
            EKeyMonitorType.PYNPUT: PynputBasedKeyMonitor,
        }[key_monitor_type]
        key_monitor_config_model = {
            EKeyMonitorType.PYNPUT: PynputBasedKeyMonitorConfigModel,
        }[key_monitor_type]
    except KeyError:
        raise ValueError(f'Unsupported key monitor type: {key_monitor_type}')

    # create key monitor
    logger.debug(f'create {key_monitor_cls.__name__}')
    key_monitor_config: BaseKeyMonitorConfigModel = key_monitor_config_model(**dict_config)  # noqa
    key_monitor: BaseKeyMonitor = key_monitor_cls(**key_monitor_config.model_dump())    # type: ignore # noqa

    return key_monitor