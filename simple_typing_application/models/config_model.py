from enum import Enum
from pydantic import BaseModel


class ESentenceGeneratorType(Enum):
    OPENAI: str = 'OPENAI'


class EUserInterfaceType(Enum):
    CONSOLE: str = 'CONSOLE'


class BaseSentenceGeneratorConfigModel(BaseModel):
    pass


class OpenAISentenceGeneratorConfigModel(BaseSentenceGeneratorConfigModel):
    model: str = 'gpt-3.5-turbo-16k'
    temperature: float = 0.7
    openai_api_key: str | None = None
    memory_size: int = 1
    max_retry: int = 5


class BaseUserInterfaceConfigModel(BaseModel):
    pass


class ConsoleUserInterfaceConfigModel(BaseUserInterfaceConfigModel):
    pass


class ConfigModel(BaseModel):
    sentence_generator_type: ESentenceGeneratorType = ESentenceGeneratorType.OPENAI  # noqa
    sentence_generator_config: dict[str, str | float | int | None] = OpenAISentenceGeneratorConfigModel().model_dump()  # noqa

    user_interface_type: EUserInterfaceType = EUserInterfaceType.CONSOLE
    user_interface_config: dict[str, str | float | int | None] = ConsoleUserInterfaceConfigModel().model_dump()  # noqa

    record_direc: str = './record'


SENTENCE_GENERATOR_TYPE_TO_CONFIG_MODEL: dict[ESentenceGeneratorType, BaseModel] = {  # noqa
    ESentenceGeneratorType.OPENAI: OpenAISentenceGeneratorConfigModel,  # type: ignore  # noqa
}

USER_INTERFACE_TYPE_TO_CONFIG_MODEL: dict[EUserInterfaceType, BaseModel] = {  # noqa
    EUserInterfaceType.CONSOLE: ConsoleUserInterfaceConfigModel,  # type: ignore  # noqa
}

# TODO: make maps immutable
