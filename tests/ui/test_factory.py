import pytest

from simple_typing_application.models.config_model import (
    EUserInterfaceType,
    BaseUserInterfaceConfigModel,
)
from simple_typing_application.ui.cui import ConsoleUserInterface
from simple_typing_application.ui.factory import create_user_interface


@pytest.mark.parametrize(
    'user_interface_type, user_interface_config, expected_class',
    [
        (
            EUserInterfaceType.CONSOLE,
            BaseUserInterfaceConfigModel(),
            ConsoleUserInterface,
        ),
    ],
)
def test_create_user_interface(
    user_interface_type: EUserInterfaceType,
    user_interface_config: BaseUserInterfaceConfigModel,
    expected_class: type,
    mocker,
):
    # mock
    # for ConsoleUserInterface
    # None

    # execute
    user_interface = create_user_interface(
        user_interface_type,
        user_interface_config,
    )

    # assert
    assert isinstance(user_interface, expected_class)
