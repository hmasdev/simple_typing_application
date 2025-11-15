from __future__ import annotations
from pydantic import BaseModel

from .key_monitor_config_model import BaseKeyMonitorConfigModel
from .sentence_generator_config_model import BaseSentenceGeneratorConfigModel
from .user_interface_config_model import BaseUserInterfaceConfigModel
from ...const.key_monitor import EKeyMonitorType
from ...const.sentence_generator import ESentenceGeneratorType
from ...const.user_interface import EUserInterfaceType


class ConfigModel(BaseModel):
    sentence_generator_type: ESentenceGeneratorType = ESentenceGeneratorType.OPENAI  # noqa
    sentence_generator_config: dict[str, str | float | int | bool | None | dict | list] = (
        BaseSentenceGeneratorConfigModel().model_dump()
    )  # noqa

    user_interface_type: EUserInterfaceType = EUserInterfaceType.CONSOLE
    user_interface_config: dict[str, str | float | int | None | dict | list] = (
        BaseUserInterfaceConfigModel().model_dump()
    )  # noqa

    key_monitor_type: EKeyMonitorType = EKeyMonitorType.PYNPUT
    key_monitor_config: dict[str, str | float | int | None | dict | list] = BaseKeyMonitorConfigModel().model_dump()  # noqa

    record_direc: str = "./record"
