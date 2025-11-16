from __future__ import annotations
from logging import getLogger, Logger

from .base import BaseUserInterface
from .cui import ConsoleUserInterface
from ..const.user_interface import EUserInterfaceType
from ..models.config_models.user_interface_config_model import (  # noqa
    BaseUserInterfaceConfigModel,
    ConsoleUserInterfaceConfigModel,
)


def _select_class_and_config_model(user_interface_type: EUserInterfaceType) -> tuple[type, type]:  # noqa
    if user_interface_type == EUserInterfaceType.CONSOLE:
        return ConsoleUserInterface, ConsoleUserInterfaceConfigModel
    else:
        raise ValueError(f"Unsupported user interface type: {user_interface_type}")  # noqa


def create_user_interface(
    user_interface_type: EUserInterfaceType,
    config: BaseUserInterfaceConfigModel,
    logger: Logger = getLogger(__name__),
) -> BaseUserInterface:
    # select user interface class and config model
    try:
        user_interface_cls, user_interface_config_model = _select_class_and_config_model(user_interface_type)  # noqa
    except NameError:
        raise ImportError(
            f"Failed to import user interface class and config model for user_interface_type={user_interface_type}"
        )  # noqa

    # create user interface
    logger.debug(f"create {user_interface_cls.__name__}")
    user_interface_config: BaseUserInterfaceConfigModel
    if isinstance(config, user_interface_config_model):
        user_interface_config = config
    else:
        user_interface_config = user_interface_config_model(**config.model_dump())  # noqa
    user_interface: BaseUserInterface = user_interface_cls(**user_interface_config.model_dump())  # type: ignore # noqa

    return user_interface
