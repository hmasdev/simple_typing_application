from enum import Enum
from pydantic import BaseModel


class ESentenceGeneratorType(Enum):
    OPENAI: str = 'OPENAI'
    HUGGINGFACE: str = 'HUGGINGFACE'
    STATIC: str = 'STATIC'


class EUserInterfaceType(Enum):
    CONSOLE: str = 'CONSOLE'


class BaseSentenceGeneratorConfigModel(BaseModel):
    pass


class OpenAISentenceGeneratorConfigModel(BaseSentenceGeneratorConfigModel):
    model: str = 'gpt-3.5-turbo-16k'
    temperature: float = 0.7
    openai_api_key: str | None = None
    memory_size: int = 0
    max_retry: int = 5


class HuggingfaceSentenceGeneratorConfigModel(BaseSentenceGeneratorConfigModel):  # noqa
    model: str = 'line-corporation/japanese-large-lm-3.6b'
    max_length: int = 100
    do_sample: bool = True
    top_k: int = 50
    top_p: float = 0.95
    device: str = 'cuda'


class StaticSentenceGeneratorConfigModel(BaseSentenceGeneratorConfigModel):
    text_kana_map: dict[str, str | None]
    is_random: bool = False


class BaseUserInterfaceConfigModel(BaseModel):
    pass


class ConsoleUserInterfaceConfigModel(BaseUserInterfaceConfigModel):
    pass


class ConfigModel(BaseModel):
    sentence_generator_type: ESentenceGeneratorType = ESentenceGeneratorType.OPENAI  # noqa
    sentence_generator_config: dict[str, str | float | int | bool | None | dict | list] = OpenAISentenceGeneratorConfigModel().model_dump()  # noqa

    user_interface_type: EUserInterfaceType = EUserInterfaceType.CONSOLE
    user_interface_config: dict[str, str | float | int | None | dict | list] = ConsoleUserInterfaceConfigModel().model_dump()  # noqa

    record_direc: str = './record'


SENTENCE_GENERATOR_TYPE_TO_CONFIG_MODEL: dict[ESentenceGeneratorType, BaseModel] = {  # noqa
    ESentenceGeneratorType.OPENAI: OpenAISentenceGeneratorConfigModel,  # type: ignore  # noqa
    ESentenceGeneratorType.HUGGINGFACE: HuggingfaceSentenceGeneratorConfigModel,  # type: ignore  # noqa
    ESentenceGeneratorType.STATIC: StaticSentenceGeneratorConfigModel,  # type: ignore  # noqa
}

USER_INTERFACE_TYPE_TO_CONFIG_MODEL: dict[EUserInterfaceType, BaseModel] = {  # noqa
    EUserInterfaceType.CONSOLE: ConsoleUserInterfaceConfigModel,  # type: ignore  # noqa
}

# TODO: make maps immutable
