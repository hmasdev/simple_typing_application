import json
from logging import getLogger, Logger
import os
from .models.config_model import (
    ConfigModel,
    BaseSentenceGeneratorConfigModel,
    BaseUserInterfaceConfigModel,
    SENTENCE_GENERATOR_TYPE_TO_CONFIG_MODEL,
    USER_INTERFACE_TYPE_TO_CONFIG_MODEL
)


def load_config(
    path: str,
    logger: Logger = getLogger(__name__),
) -> tuple[ConfigModel, BaseSentenceGeneratorConfigModel, BaseUserInterfaceConfigModel]:  # noqa
    '''Load config file.

    Args:
        path (str): path to config file.
        logger (Logger, optional): logger. Defaults to getLogger(__name__).

    Raises:
        ValueError: unsupported file type.

    Returns:
        ConfigModel: config model.
        BaseSentenceGeneratorConfigModel: sentence generator config model.
        BaseUserInterfaceConfigModel: user interface config model.
    '''  # noqa
    logger.debug(f'load config from {path}')

    # load config
    if os.path.splitext(path)[1] == '.json':
        logger.debug('load json config')
        try:
            config = ConfigModel(**json.load(open(path, 'r', encoding='utf-8')))  # type: ignore  # noqa
        except FileNotFoundError:
            logger.warning(f'config file not found: {path}. So use default config.')  # noqa
            config = ConfigModel()
        sentence_generator_config = SENTENCE_GENERATOR_TYPE_TO_CONFIG_MODEL[config.sentence_generator_type](**config.sentence_generator_config)  # type: ignore  # noqa
        user_interface_config = USER_INTERFACE_TYPE_TO_CONFIG_MODEL[config.user_interface_type](**config.user_interface_config)  # type: ignore  # noqa
    elif os.path.splitext(path)[1] in ['.yaml', '.yml']:
        logger.debug('load yaml config')
        raise NotImplementedError('yaml is not supported yet.')
    else:
        raise ValueError(f'Unsupported file type: {os.path.splitext(path)[1]}')

    logger.debug(f'config: {config}')
    logger.debug(f'sentence_generator_config: {sentence_generator_config}')
    logger.debug(f'user_interface_config: {user_interface_config}')

    return config, sentence_generator_config, user_interface_config
