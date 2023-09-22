from logging import getLogger, Logger

from .base import BaseUserInterface
from .cui import ConsoleUserInterface
from ..models.config_model import (
    EUserInterfaceType,
    BaseUserInterfaceConfigModel,
)


def create_user_interface(
    user_interface_type: EUserInterfaceType,
    user_interface_config: BaseUserInterfaceConfigModel,
    logger: Logger = getLogger(__name__),
) -> BaseUserInterface:

    # select user interface class
    try:
        user_interface_cls = {
            EUserInterfaceType.CONSOLE: ConsoleUserInterface,
        }[user_interface_type]
    except KeyError:
        raise ValueError(
            f'Unsupported user interface type: {user_interface_type}')

    # create user interface
    logger.debug(f'create {user_interface_cls.__name__}')
    user_interface: BaseUserInterface = user_interface_cls(**user_interface_config.model_dump())    # type: ignore # noqa

    return user_interface
