import json
from logging import getLogger, Logger
import os
from .models.config_models import ConfigModel


def load_config(
    path: str,
    logger: Logger = getLogger(__name__),
) -> ConfigModel:  # noqa
    """Load config file.

    Args:
        path (str): path to config file.
        logger (Logger, optional): logger. Defaults to getLogger(__name__).

    Raises:
        ValueError: unsupported file type.

    Returns:
        ConfigModel: config model.
    """  # noqa
    logger.debug(f"load config from {path}")

    # load config
    if os.path.splitext(path)[1] == ".json":
        logger.debug("load json config")
        try:
            config = ConfigModel(**json.load(open(path, "r", encoding="utf-8")))  # type: ignore  # noqa
        except FileNotFoundError:
            logger.warning(f"config file not found: {path}. So use default config.")  # noqa
            config = ConfigModel()
    elif os.path.splitext(path)[1] in [".yaml", ".yml"]:
        logger.debug("load yaml config")
        raise NotImplementedError("yaml is not supported yet.")
    else:
        raise ValueError(f"Unsupported file type: {os.path.splitext(path)[1]}")

    logger.debug(f"config: {config}")
    return config
