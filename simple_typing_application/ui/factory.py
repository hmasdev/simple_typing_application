from logging import getLogger, Logger

from .base import BaseUserInterface
from .cui import ConsoleUserInterface
from ..const.user_interface import EUserInterfaceType
from ..models.config_models.user_interface_config_model import (  # noqa
    BaseUserInterfaceConfigModel,
    ConsoleUserInterfaceConfigModel,
)


def create_user_interface(
    user_interface_type: EUserInterfaceType,
    dict_config: dict[str, str | float | int | bool | None | dict | list],
    logger: Logger = getLogger(__name__),
) -> BaseUserInterface:

    # select user interface class and config model
    try:
        user_interface_cls = {
            EUserInterfaceType.CONSOLE: ConsoleUserInterface,
        }[user_interface_type]
        user_interface_config_model = {
            EUserInterfaceType.CONSOLE: ConsoleUserInterfaceConfigModel,
        }[user_interface_type]
    except KeyError:
        raise ValueError(
            f'Unsupported user interface type: {user_interface_type}')

    # create user interface
    logger.debug(f'create {user_interface_cls.__name__}')
    user_interface_config: BaseUserInterfaceConfigModel = user_interface_config_model(**dict_config)  # noqa
    user_interface: BaseUserInterface = user_interface_cls(**user_interface_config.model_dump())    # type: ignore # noqa

    return user_interface
