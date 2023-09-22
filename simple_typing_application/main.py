from logging import basicConfig, DEBUG, getLogger, INFO, Logger

import click

from .config import load_config
from .sentence_generator import create_sentence_generator
from .typing_game import TypingGame
from .ui import create_user_interface


@click.command()
@click.option('--config-path', '-c', default='./config.json', help='path to config file. Defaults to ./config.json')  # noqa
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
