from logging import getLogger, Logger

from .base import BaseSentenceGenerator  # noqa
from .huggingface_sentence_generator import HuggingfaceSentenceGenerator  # noqa
from .openai_sentence_generator import OpenaiSentenceGenerator  # noqa
from .static_sentence_generator import StaticSentenceGenerator  # noqa
from ..models.config_model import (
    ESentenceGeneratorType,
    BaseSentenceGeneratorConfigModel,
)


def create_sentence_generator(
    sentence_generator_type: ESentenceGeneratorType,
    sentence_generator_config: BaseSentenceGeneratorConfigModel,
    logger: Logger = getLogger(__name__),
) -> BaseSentenceGenerator:

    # select sentence generator class
    try:
        sentence_generator_cls = {
            ESentenceGeneratorType.OPENAI: OpenaiSentenceGenerator,
            ESentenceGeneratorType.HUGGINGFACE: HuggingfaceSentenceGenerator,
            ESentenceGeneratorType.STATIC: StaticSentenceGenerator,
        }[sentence_generator_type]
    except KeyError:
        raise ValueError(f'Unsupported sentence generator type: {sentence_generator_type}')  # noqa

    # create sentence generator
    logger.debug(f'create {sentence_generator_cls.__name__}')
    sentence_generator: BaseSentenceGenerator = sentence_generator_cls(**sentence_generator_config.model_dump())    # type: ignore # noqa

    return sentence_generator
