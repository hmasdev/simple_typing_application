from __future__ import annotations
import pytest

from simple_typing_application.const.user_interface import EUserInterfaceType
from simple_typing_application.models.config_models.user_interface_config_model import (  # noqa
    ConsoleUserInterfaceConfigModel,
)
from simple_typing_application.ui.cui import ConsoleUserInterface
from simple_typing_application.ui.factory import (
    create_user_interface,
    _select_class_and_config_model,
)


@pytest.mark.parametrize(
    'user_interface_type, expected_class, expected_config_model',
    [
        (
            EUserInterfaceType.CONSOLE,
            ConsoleUserInterface,
            ConsoleUserInterfaceConfigModel,
        ),
    ],
)
def test_select_class_and_config_model(
    user_interface_type: EUserInterfaceType,
    expected_class: type,
    expected_config_model: type,
):

    # execute
    user_interface_cls, user_interface_config_model = _select_class_and_config_model(user_interface_type)  # noqa

    # assert
    assert user_interface_cls is expected_class
    assert user_interface_config_model is expected_config_model


def test_select_class_and_config_model_raise_value_error():
    # execute
    with pytest.raises(ValueError):
        _select_class_and_config_model('invalid_key_monitor_type')  # type: ignore  # noqa


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


def test_create_user_interface_raise_import_error(mocker):

    # mock
    mocker.patch(
        'simple_typing_application.ui.factory._select_class_and_config_model',
        side_effect=NameError,
    )

    # execute
    with pytest.raises(ImportError):
        create_user_interface(
            EUserInterfaceType.CONSOLE,
            {},
        )


def test_create_user_interface_raise_value_error(mocker):

    # mock
    mocker.patch(
        'simple_typing_application.ui.factory._select_class_and_config_model',
        side_effect=ValueError,
    )

    # execute
    with pytest.raises(ValueError):
        create_user_interface(
            'invalid_user_interface_type',  # type: ignore
            {},
        )
