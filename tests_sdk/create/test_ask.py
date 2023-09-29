import logging
import pytest
from sdk.create.ask import (
    ask_module_name_for_create,
    ask_class_name_for_create,
)
from sdk.enum import EComponent


@pytest.mark.sdk
@pytest.mark.parametrize(
    'conponent, input_returns, expected_number_of_calls_of_input, expected_error_messages',  # noqa
    [
        (
            EComponent.KEY_MONITOR,
            ['hoge'],
            1,
            [],
        ),
        (
            EComponent.UI,
            ['', 'hoge'],
            2,
            ['Module name must not be empty.'],
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            ['1hoge', 'hoge'],
            2,
            ['Module name must start with alphabet or underscore.'],
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            ['hoge!', 'hoge'],
            2,
            ['Module name must be composed of alphabets, numbers, and underscores.'],  # noqa
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            ['__init__', 'hoge'],
            2,
            ['Module name must not be duplicated.'],
        ),
        (
            EComponent.UI,
            ['__init__', 'hoge'],
            2,
            ['Module name must not be duplicated.'],
        ),
        (
            EComponent.KEY_MONITOR,
            ['__init__', 'hoge'],
            2,
            ['Module name must not be duplicated.'],
        ),
        (
            EComponent.UI,
            ['', '0hoge', 'hoge'],
            3,
            ['Module name must not be empty.', 'Module name must start with alphabet or underscore.'],  # noqa
        ),
    ]
)
def test_ask_module_name_for_create(
    conponent: EComponent,
    input_returns: list[str],
    expected_number_of_calls_of_input: int,
    expected_error_messages: list[str],
    caplog,
    mocker,
):

    # mock
    mock_input = mocker.patch('builtins.input', side_effect=input_returns)

    # exec
    actual = ask_module_name_for_create(conponent)
    extracted_logs = [
        (record, msg)
        for record in caplog.record_tuples
        for msg in expected_error_messages
        if msg in record[-1]
    ]

    # assert
    assert mock_input.call_count == expected_number_of_calls_of_input
    assert len(extracted_logs) == len(expected_error_messages)  # NOTE: if this assertion fails, there may be duplicate error messages.  # noqa
    assert all([x[0][1] == logging.ERROR for x in extracted_logs])
    assert [x[-1] for x in extracted_logs] == expected_error_messages
    assert actual == input_returns[-1]


@pytest.mark.sdk
@pytest.mark.parametrize(
    'component, input_returns, expected_number_of_calls_of_input, expected_error_messages',  # noqa
    [
        (
            EComponent.KEY_MONITOR,
            ['hoge'],
            1,
            [],
        ),
        (
            EComponent.UI,
            ['', 'hoge'],
            2,
            ['Class name must not be empty.'],
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            ['1hoge', 'hoge'],
            2,
            ['Class name must start with alphabet or underscore.'],
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            ['__hoge', 'hoge'],
            2,
            ['Class name must not start with "__".'],
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            ['hoge!', 'hoge'],
            2,
            ['Class name must be composed of alphabets, numbers, and underscores.'],  # noqa
        ),
        (
            EComponent.UI,
            ['', '0hoge', 'hoge'],
            3,
            ['Class name must not be empty.', 'Class name must start with alphabet or underscore.'],  # noqa
        )
    ]
)
def test_ask_class_name_for_create(
    component: EComponent,
    input_returns: list[str],
    expected_number_of_calls_of_input: int,
    expected_error_messages: list[str],
    caplog,
    mocker,
):
    # mock
    mock_input = mocker.patch('builtins.input', side_effect=input_returns)

    # exec
    actual = ask_class_name_for_create(component)
    extracted_logs = [
        # NOTE: extract logs which contain expected_error_messages.
        (record, msg)
        for record in caplog.record_tuples
        for msg in set(expected_error_messages)
        if msg in record[-1]
    ]

    # assert
    assert mock_input.call_count == expected_number_of_calls_of_input
    assert len(extracted_logs) == len(expected_error_messages)   # NOTE: if this assertion fails, there may be duplicate error messages.  # noqa
    assert all([x[0][1] == logging.ERROR for x in extracted_logs])
    assert [x[-1] for x in extracted_logs] == expected_error_messages
    assert actual == input_returns[-1]
