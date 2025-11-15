from __future__ import annotations
from pydantic import BaseModel

from .key_monitor_config_model import (
    BaseKeyMonitorConfigModel,
    PynputBasedKeyMonitorConfigModel,
    SSHKeyboardBasedKeyMonitorConfigModel,
)
from .sentence_generator_config_model import (
    BaseSentenceGeneratorConfigModel,
    HuggingfaceSentenceGeneratorConfigModel,
    OpenAISentenceGeneratorConfigModel,
    StaticSentenceGeneratorConfigModel,
)
from .user_interface_config_model import (
    BaseUserInterfaceConfigModel,
    ConsoleUserInterfaceConfigModel,
)
from ...const.key_monitor import EKeyMonitorType
from ...const.sentence_generator import ESentenceGeneratorType
from ...const.user_interface import EUserInterfaceType


class ConfigModel(BaseModel):
    sentence_generator_type: ESentenceGeneratorType = ESentenceGeneratorType.OPENAI  # noqa
    sentence_generator_config: (
        BaseSentenceGeneratorConfigModel
        | HuggingfaceSentenceGeneratorConfigModel
        | OpenAISentenceGeneratorConfigModel
        | StaticSentenceGeneratorConfigModel
    ) = BaseSentenceGeneratorConfigModel()

    user_interface_type: EUserInterfaceType = EUserInterfaceType.CONSOLE
    user_interface_config: BaseUserInterfaceConfigModel | ConsoleUserInterfaceConfigModel = (
        BaseUserInterfaceConfigModel()
    )

    key_monitor_type: EKeyMonitorType = EKeyMonitorType.PYNPUT
    key_monitor_config: (
        BaseKeyMonitorConfigModel | PynputBasedKeyMonitorConfigModel | SSHKeyboardBasedKeyMonitorConfigModel
    ) = BaseKeyMonitorConfigModel()

    record_direc: str = "./record"
