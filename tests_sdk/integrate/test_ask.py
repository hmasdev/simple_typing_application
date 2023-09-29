import logging
import os
from types import ModuleType
from typing import Callable
from unittest.mock import MagicMock
import pytest
from sdk.const import COMPONENT_SUBPACKAGE_DIR_MAP, COMPONENT_SUBPACKAGE_MAP
from sdk.enum import EComponent
from sdk.integrate.ask import (
    ask_module_name,
    ask_class_name,
    ask_class_alias,
    ask_config_model_name,
)


def assert_true(b: bool | None):
    assert isinstance(b, bool)
    assert b


@pytest.mark.sdk
@pytest.mark.parametrize(
    'component, input_returns, mock_func_os_path_exists, mock_func_os_path_isfile, mock_func_import_module, expected_error_messages',  # noqa
    # NOTE: input_returns[-1] is the expected return value of ask_module_name().  # noqa
    [
        (
            EComponent.KEY_MONITOR,
            ['hoge'],
            lambda x: {
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.KEY_MONITOR], 'hoge.py'): True,  # noqa
            }.get(x),
            lambda x: {
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.KEY_MONITOR], 'hoge.py'): True,  # noqa
            }.get(x),
            lambda x: assert_true({
                f"{COMPONENT_SUBPACKAGE_MAP[EComponent.KEY_MONITOR]}.hoge": True,  # noqa
            }.get(x)),
            [],
        ),
        (
            EComponent.UI,
            ['hoge', 'fuga', 'piyo'],
            lambda x: {
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.UI], 'hoge.py'): True,  # noqa
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.UI], 'fuga.py'): True,  # noqa
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.UI], 'piyo.py'): True,  # noqa
            }.get(x),
            lambda x: {
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.UI], 'hoge.py'): True,  # noqa
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.UI], 'fuga.py'): False,  # noqa
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.UI], 'piyo.py'): True,  # noqa
            }.get(x),
            lambda x: assert_true({
                f"{COMPONENT_SUBPACKAGE_MAP[EComponent.UI]}.hoge": False,  # noqa
                f"{COMPONENT_SUBPACKAGE_MAP[EComponent.UI]}.fuga": True,  # noqa
                f"{COMPONENT_SUBPACKAGE_MAP[EComponent.UI]}.piyo": True,  # noqa
            }.get(x)),
            [
                'Failed to import the given module. Check and fix the module',
                "Given module name is not a file but a package.",
            ],
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            ['hoge', 'fuga', 'piyo'],
            lambda x: {
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], 'hoge.py'): True,  # noqa
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], 'fuga.py'): False,  # noqa
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], 'piyo.py'): True,  # noqa
            }.get(x),
            lambda x: {
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], 'hoge.py'): False,  # noqa
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], 'fuga.py'): True,  # noqa
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], 'piyo.py'): True,  # noqa
            }.get(x),
            lambda x: assert_true({
                f"{COMPONENT_SUBPACKAGE_MAP[EComponent.SENTENCE_GENERATOR]}.hoge": False,  # noqa
                f"{COMPONENT_SUBPACKAGE_MAP[EComponent.SENTENCE_GENERATOR]}.fuga": True,  # noqa
                f"{COMPONENT_SUBPACKAGE_MAP[EComponent.SENTENCE_GENERATOR]}.piyo": True,  # noqa
            }.get(x)),
            [
                "Given module name is not a file but a package.",
                'Module not found. Check the name of the module or create the module.',  # noqa
            ],
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            ['hoge', 'fuga', 'piyo', 'hogehoge'],
            lambda x: {
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], 'hoge.py'): False,  # noqa
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], 'fuga.py'): False,  # noqa
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], 'piyo.py'): False,  # noqa
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], 'hogehoge.py'): True,  # noqa
            }.get(x),
            lambda x: {
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], 'hoge.py'): True,  # noqa
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], 'fuga.py'): False,  # noqa
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], 'piyo.py'): False,  # noqa
                os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], 'hogehoge.py'): True,  # noqa
            }.get(x),
            lambda x: assert_true({
                f"{COMPONENT_SUBPACKAGE_MAP[EComponent.SENTENCE_GENERATOR]}.hoge": False,  # noqa
                f"{COMPONENT_SUBPACKAGE_MAP[EComponent.SENTENCE_GENERATOR]}.fuga": True,  # noqa
                f"{COMPONENT_SUBPACKAGE_MAP[EComponent.SENTENCE_GENERATOR]}.piyo": False,  # noqa
                f"{COMPONENT_SUBPACKAGE_MAP[EComponent.SENTENCE_GENERATOR]}.hogehoge": True,  # noqa
            }.get(x)),
            [
                'Module not found. Check the name of the module or create the module.',  # noqa
                'Module not found. Check the name of the module or create the module.',  # noqa
                'Module not found. Check the name of the module or create the module.',  # noqa
            ],
        ),
    ]
)
def test_ask_module_name(
    component: EComponent,
    input_returns: list[str],
    mock_func_os_path_exists: Callable[[str], bool],
    mock_func_os_path_isfile: Callable[[str], bool],
    mock_func_import_module: Callable[[str], None],
    expected_error_messages: list[str],
    caplog,
    mocker
):
    # mock
    mock_input = mocker.patch('builtins.input', side_effect=input_returns)
    mock_os_path_exists = mocker.patch('sdk.integrate.ask.os.path.exists', side_effect=mock_func_os_path_exists)  # noqa
    mock_os_path_isfile = mocker.patch('sdk.integrate.ask.os.path.isfile', side_effect=mock_func_os_path_isfile)  # noqa
    mock_import_module = mocker.patch('sdk.integrate.ask.import_module', side_effect=mock_func_import_module)  # noqa

    # exec
    actual = ask_module_name(component)
    extracted_logs = [
        # NOTE: extract logs which contain expected_error_messages.
        (record, msg)
        for record in caplog.record_tuples
        for msg in set(expected_error_messages)
        if msg in record[-1]
    ]

    # assert
    assert actual == input_returns[-1]
    assert mock_input.call_count == len(input_returns)
    assert len(extracted_logs) == len(expected_error_messages)  # NOTE: if this assertion fails, there may be duplicate error messages.  # noqa
    assert all([x[0][1] == logging.ERROR for x in extracted_logs])
    assert [x[-1] for x in extracted_logs] == expected_error_messages


@pytest.mark.sdk
@pytest.mark.parametrize(
    'component, mock_module, input_returns, expected_error_messages',  # noqa
    # NOTE: input_returns[-1] is the expected return value of ask_class_name().  # noqa
    [
        (
            EComponent.KEY_MONITOR,
            MagicMock(spec=ModuleType, **{'ValidClass': MagicMock(spec=type)}),
            [
                'ValidClass',
            ],
            [],
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            MagicMock(spec=ModuleType, **{'Hoge': MagicMock(spec=int), 'ValidClass': MagicMock(spec=type)}),  # noqa
            [
                'Hoge',  # NOTE: Case that module has the attribute but it is not a class.  # noqa
                'ValidClass',
            ],
            [
                'Class not found. Check the name of the class or create the class.',  # noqa
            ],
        ),
        (
            EComponent.UI,
            MagicMock(spec=ModuleType, **{'Hoge': MagicMock(spec=int), 'ValidClass': MagicMock(spec=type)}),  # noqa
            [
                'Fuga',  # NOTE: Case that module does not have the attribute.  # noqa
                'ValidClass',
            ],
            [
                'Class not found. Check the name of the class or create the class.',  # noqa
            ],
        )
    ]
)
def test_ask_class_name(
    component: EComponent,
    mock_module: ModuleType,
    input_returns: list[str],
    expected_error_messages: list[str],
    caplog,
    mocker,
):
    # mock
    mock_input = mocker.patch('builtins.input', side_effect=input_returns)

    # exec
    actual = ask_class_name(component, mock_module)
    extracted_logs = [
        # NOTE: extract logs which contain expected_error_messages.
        (record, msg)
        for record in caplog.record_tuples
        for msg in set(expected_error_messages)
        if msg in record[-1]
    ]

    # assert
    assert actual == input_returns[-1]
    assert mock_input.call_count == len(input_returns)
    assert len(extracted_logs) == len(expected_error_messages)
    assert all([x[0][1] == logging.ERROR for x in extracted_logs])
    assert [x[-1] for x in extracted_logs] == expected_error_messages


@pytest.mark.sdk
@pytest.mark.parametrize(
    'component, class_name, input_returns, expected_error_messages',  # noqa
    # NOTE: input_returns[-1] is the expected return value of ask_class_alias().  # noqa
    #       When input_returns[-1] is "", the expected return value is class_name.capitalize().  # noqa
    [
        (
            EComponent.KEY_MONITOR,
            'ValidClass',
            [
                '',
            ],
            [],
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            'ValidClass',
            [
                'ValidAlias',
            ],
            [],
        ),
        (
            EComponent.UI,
            'ValidClass',
            [
                '1InvalidAlias',
                'ValidAlias',
            ],
            [
                'Alias must start with alphabet or underscore.',
            ],
        ),
        (
            EComponent.UI,
            'ValidClass',
            [
                '__InvalidAlias',
                'ValidAlias',
            ],
            [
                'Alias must not start with "__".',
            ],
        ),
        (
            EComponent.KEY_MONITOR,
            'ValidClass',
            [
                'PYNPUT',
                'ValidAlias',
            ],
            [
                'Alias has already been used. Try another one.',
            ],
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            'ValidClass',
            [
                'OPENAI',
                'ValidAlias',
            ],
            [
                'Alias has already been used. Try another one.',
            ],
        ),
        (
            EComponent.UI,
            'ValidClass',
            [
                'CONSOLE',
                'ValidAlias',
            ],
            [
                'Alias has already been used. Try another one.',
            ],
        ),
        (
            EComponent.UI,
            'ValidClass',
            [
                'InvalidAlias!',
                'ValidAlias',
            ],
            [
                'Alias must be composed of alphabets, numbers, and underscores.',  # noqa
            ],
        ),
    ]
)
def test_class_alias(
    component: EComponent,
    class_name: str,
    input_returns: list[str],
    expected_error_messages: list[str],
    caplog,
    mocker,
):
    # mock
    mock_input = mocker.patch('builtins.input', side_effect=input_returns)

    # exec
    actual = ask_class_alias(component, class_name)
    extracted_logs = [
        # NOTE: extract logs which contain expected_error_messages.
        (record, msg)
        for record in caplog.record_tuples
        for msg in set(expected_error_messages)
        if msg in record[-1]
    ]

    # assert
    assert actual == input_returns[-1] if input_returns[-1] != '' else class_name.capitalize()  # noqa
    assert mock_input.call_count == len(input_returns)
    assert len(extracted_logs) == len(expected_error_messages)
    assert all([x[0][1] == logging.ERROR for x in extracted_logs])
    assert [x[-1] for x in extracted_logs] == expected_error_messages


@pytest.mark.sdk
@pytest.mark.parametrize(
    'component, class_name, input_returns, expected_error_messages',  # noqa
    # NOTE: input_returns[-1] is the expected return value of ask_config_model_name().  # noqa
    #       When input_returns[-1] is "", the expected return value is f'{class_name}ConfigModel'.  # noqa
    [
        (
            EComponent.KEY_MONITOR,
            'ValidClass',
            [
                '',
            ],
            [],
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            'ValidClass',
            [
                'ValidConfigModel',
            ],
            [],
        ),
        (
            EComponent.UI,
            'ValidClass',
            [
                '1InvalidConfigModel',
                'ValidConfigModel',
            ],
            [
                'Config model name must start with alphabet or underscore.',
            ],
        ),
        (
            EComponent.UI,
            'ValidClass',
            [
                '__InvalidConfigModel',
                'ValidConfigModel',
            ],
            [
                'Config model name must not start with "__".',
            ],
        ),
        (
            EComponent.KEY_MONITOR,
            'ValidClass',
            [
                'PynputBasedKeyMonitorConfigModel',
                'ValidConfigModel',
            ],
            [
                'Config model name has already been used. Try another one.',
            ],
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            'ValidClass',
            [
                'OpenAISentenceGeneratorConfigModel',
                'ValidConfigModel',
            ],
            [
                'Config model name has already been used. Try another one.',
            ],
        ),
        (
            EComponent.UI,
            'ValidClass',
            [
                'ConsoleUserInterfaceConfigModel',
                'ValidConfigModel',
            ],
            [
                'Config model name has already been used. Try another one.',
            ],
        ),
        (
            EComponent.UI,
            'ValidClass',
            [
                'InvalidConfigModel!',
                'ValidConfigModel',
            ],
            [
                'Config model name must be composed of alphabets, numbers, and underscores.',  # noqa
            ],
        ),
    ]
)
def test_ask_config_model_name(
    component: EComponent,
    class_name: str,
    input_returns: list[str],
    expected_error_messages: list[str],
    caplog,
    mocker,
):
    # mock
    mock_input = mocker.patch('builtins.input', side_effect=input_returns)

    # exec
    actual = ask_config_model_name(component, class_name)
    extracted_logs = [
        # NOTE: extract logs which contain expected_error_messages.
        (record, msg)
        for record in caplog.record_tuples
        for msg in set(expected_error_messages)
        if msg in record[-1]
    ]

    # assert
    assert actual == input_returns[-1] if input_returns[-1] != '' else f'{class_name}ConfigModel'  # noqa
    assert mock_input.call_count == len(input_returns)
    assert len(extracted_logs) == len(expected_error_messages)
    assert all([x[0][1] == logging.ERROR for x in extracted_logs])
    assert [x[-1] for x in extracted_logs] == expected_error_messages
