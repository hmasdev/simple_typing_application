from logging import basicConfig, DEBUG, getLogger, INFO, Logger

import click

from .config import load_config
from .models.config_model import (
    ESentenceGeneratorType,
    EUserInterfaceType,
    BaseSentenceGeneratorConfigModel,
    BaseUserInterfaceConfigModel
)
from .sentence_generator.base import BaseSentenceGenerator
from .sentence_generator.openai_sentence_generator import OpenaiSentenceGenerator  # noqa
from .typing_game import TypingGame
from .ui.base import BaseUserInterface
from .ui.cui import ConsoleUserInterface


def create_sentence_generator(
    sentence_generator_type: ESentenceGeneratorType,
    sentence_generator_config: BaseSentenceGeneratorConfigModel,
    logger: Logger = getLogger(__name__),
) -> BaseSentenceGenerator:
    if sentence_generator_type == ESentenceGeneratorType.OPENAI:
        logger.debug('create OpenaiSentenceGenerator')
        return OpenaiSentenceGenerator(**sentence_generator_config.model_dump())  # noqa
    else:
        raise ValueError(f'Unsupported sentence generator type: {sentence_generator_type}')  # noqa


def create_user_interface(
    user_interface_type: EUserInterfaceType,
    user_interface_config: BaseUserInterfaceConfigModel,
    logger: Logger = getLogger(__name__),
) -> BaseUserInterface:
    if user_interface_type == EUserInterfaceType.CONSOLE:
        logger.debug('create ConsoleUserInterface')
        return ConsoleUserInterface(**user_interface_config.model_dump())
    else:
        raise ValueError(f'Unsupported user interface type: {user_interface_type}')  # noqa


@click.command()
@click.option('--config-path', '-c', default='./config.json', help='path to config file.')  # noqa
@click.option('--debug', '-d', is_flag=True, help='debug mode.')
def main(config_path: str, debug: bool):

    # set log level
    if debug:
        basicConfig(level=DEBUG)
    else:
        basicConfig(level=INFO)

    # load config
    config, sentence_generator_config, user_interface_config = load_config(config_path)  # noqa

    # initialize
    sentence_generator = create_sentence_generator(config.sentence_generator_type, sentence_generator_config)  # noqa
    ui = create_user_interface(config.user_interface_type, user_interface_config)  # noqa
    record_direc = config.record_direc

    game = TypingGame(sentence_generator, ui, record_direc)
    game.start()


if __name__ == "__main__":
    main()
