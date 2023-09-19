import os
import pytest
from simple_typing_application.models.config_model import (
    ConfigModel,
    OpenAISentenceGeneratorConfigModel,
    ConsoleUserInterfaceConfigModel,
)
from simple_typing_application.config import load_config


def test_load_config_json(mocker):

    # mock
    mock_open = mocker.patch('builtins.open')
    mock_json_load = mocker.patch('simple_typing_application.config.json.load')  # noqa
    mock_open.return_value = None
    mock_json_load.return_value = {
        "sentence_generator_type": "OPENAI",
        "sentence_generator_config": {
            "model": "gpt-3.5-turbo-16k",
            "temperature": 0.7,
            "openai_api_key": "HERE_IS_YOUR_API_KEY",
            "memory_size": 1,
            "max_retry": 5
        },
        "user_interface_type": "CONSOLE",
        "user_interface_config": {},
        "record_direc": "./record"
    }

    # preparation
    path = 'dummy.json'
    expected = (
        ConfigModel(**mock_json_load.return_value),
        OpenAISentenceGeneratorConfigModel(**mock_json_load.return_value['sentence_generator_config']),  # noqa
        ConsoleUserInterfaceConfigModel(**mock_json_load.return_value['user_interface_config']),  # noqa
    )

    # run
    actual = load_config(path)

    # assert
    assert actual == expected


def test_load_config_json_not_found(mocker):

    # mock
    mocker.patch('builtins.open', side_effect=FileNotFoundError)

    # preparation
    path = 'does_not_exist.json'
    expected = (
        ConfigModel(),
        OpenAISentenceGeneratorConfigModel(),
        ConsoleUserInterfaceConfigModel(),
    )

    # run
    assert not os.path.exists(path)
    actual = load_config(path)

    # assert
    assert actual == expected


def test_load_config_yaml(mocker):

    # preparation
    path = 'dummy.yaml'

    # run
    with pytest.raises(NotImplementedError):
        load_config(path)


def test_load_config_unsupported_file_type(mocker):

    # preparation
    path = 'dummy.txt'

    # run
    with pytest.raises(ValueError):
        load_config(path)
