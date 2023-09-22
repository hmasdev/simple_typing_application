import pytest

from simple_typing_application.const.user_interface import EUserInterfaceType
from simple_typing_application.models.config_models.user_interface_config_model import (
    BaseUserInterfaceConfigModel,
    ConsoleUserInterfaceConfigModel,
)
from simple_typing_application.ui.cui import ConsoleUserInterface
from simple_typing_application.ui.factory import create_user_interface


@pytest.mark.parametrize(
    'user_interface_type, user_interface_config_dict, expected_class',
    [
        (
            EUserInterfaceType.CONSOLE,
            ConsoleUserInterfaceConfigModel().model_dump(),
            ConsoleUserInterface,
        ),
        (
            EUserInterfaceType.CONSOLE,
            {},
            ConsoleUserInterface,
        ),
    ],
)
def test_create_user_interface(
    user_interface_type: EUserInterfaceType,
    user_interface_config_dict: dict[str, str | float | int | bool | None | dict | list],  # noqa
    expected_class: type,
    mocker,
):
    # mock
    # for ConsoleUserInterface
    # None

    # execute
    user_interface = create_user_interface(
        user_interface_type,
        user_interface_config_dict,
    )

    # assert
    assert isinstance(user_interface, expected_class)
