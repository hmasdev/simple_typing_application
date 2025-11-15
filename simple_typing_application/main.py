import logging

import click

from .config import load_config
from .key_monitor import create_key_monitor
from .sentence_generator import create_sentence_generator
from .typing_game import TypingGame
from .ui import create_user_interface


@click.command()
@click.option("--config-path", "-c", default="./config.json", help="path to config file. Defaults to ./config.json")  # noqa
@click.option("--log-level", "-l", default="INFO", help="log level. Defaults to INFO.")  # noqa
@click.option("--debug", "-d", is_flag=True, help="debug mode.")
def main(
    config_path: str,
    log_level: str,
    debug: bool,
    logger: logging.Logger = logging.getLogger(__name__),
):
    # set log level
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    elif log_level == "DEBUG":
        logging.basicConfig(level=logging.DEBUG)
    elif log_level == "INFO":
        logging.basicConfig(level=logging.INFO)
    elif log_level == "WARNING":
        logging.basicConfig(level=logging.WARNING)
    elif log_level == "ERROR":
        logging.basicConfig(level=logging.ERROR)
    elif log_level == "CRITICAL":
        logging.basicConfig(level=logging.CRITICAL)
    else:
        logging.basicConfig(level=logging.INFO)
        logger.warning(f"invalid log level: {log_level}. Set to INFO")

    # load config
    config = load_config(config_path)  # noqa

    # initialize
    key_monitor = create_key_monitor(config.key_monitor_type, config.key_monitor_config)  # noqa
    sentence_generator = create_sentence_generator(config.sentence_generator_type, config.sentence_generator_config)  # noqa
    ui = create_user_interface(config.user_interface_type, config.user_interface_config)  # noqa
    record_direc = config.record_direc

    game = TypingGame(sentence_generator, key_monitor, ui, record_direc)
    game.start()


if __name__ == "__main__":
    main()
