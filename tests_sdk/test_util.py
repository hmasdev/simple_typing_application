from functools import partial
from typing import Callable, Any
from unittest import mock
import pytest
from sdk.util import (
    input_until_valid,
    error_detection_validator_deco,
    integrate_validators,
)


@pytest.mark.sdk
@pytest.mark.parametrize(
    'input_returns, prompt, is_valid, callback, expected_loop_count, expected_return',  # noqa
    [
        (['input'], 'prompt1', None, None, 1, 'input'),
        (['input1', 'input2', 'input3'], 'prompt2', lambda s: s == 'input3', None, 3, 'input3'),  # noqa
        (['input'], 'prompt3', None, lambda s: s+s, 1, 'inputinput'),
        (['input1', 'input2', 'input3'], 'prompt4', lambda s: s == 'input3', lambda s: s+s, 3, 'input3input3'),  # noqa
    ]
)
def test_input_until_valid(
    input_returns: list[str],
    prompt: str,
    is_valid: Callable[[str], bool] | None,
    callback: Callable[[str], Any] | None,
    expected_loop_count: int,
    expected_return: str,
    mocker
):

    # mock
    mock_input = mocker.patch('builtins.input', side_effect=input_returns)  # noqa

    # execute
    actual = input_until_valid(
        prompt=prompt,
        is_valid=is_valid,
        callback=callback,
    )

    # assert
    assert mock_input.call_count == expected_loop_count
    assert mock_input.call_args_list == [mock.call(prompt)] * expected_loop_count  # noqa
    assert actual == expected_return


@pytest.mark.sdk
def test_error_detection_validator_deco():

    # preparation
    @error_detection_validator_deco
    def func(x: int) -> None:
        if x <= 0:
            raise ValueError('x must be positive')

    # execute
    assert func.__name__ == 'func'
    assert func(1)
    assert not func(-1)


@pytest.mark.sdk
def test_integrate_validators(caplog):

    # preparation
    expected_number_of_log = 0

    def x_is_smaller_than_y(x: int, y: int) -> bool:
        return x < y

    # case 1: single validator and single error message
    validator1 = integrate_validators(
        is_valid=partial(x_is_smaller_than_y, y=1),
        error_message='x must be smaller than 1',
    )
    # valid
    assert validator1(0)
    assert len(caplog.record_tuples) == expected_number_of_log
    # invalid
    assert not validator1(1)
    expected_number_of_log += 1
    assert len(caplog.record_tuples) == expected_number_of_log
    assert 'x must be smaller than 1' in caplog.record_tuples[-1][2]

    # case 2: multiple validators and single error messages
    validator2 = integrate_validators(
        is_valid=(
            partial(x_is_smaller_than_y, y=2),
            partial(x_is_smaller_than_y, y=1),
        ),
        error_message='x must be smaller than 1',
    )
    # valid
    assert validator2(0)
    assert len(caplog.record_tuples) == expected_number_of_log
    # invalid
    assert not validator2(1)
    expected_number_of_log += 1
    assert len(caplog.record_tuples) == expected_number_of_log
    assert 'x must be smaller than 1' in caplog.record_tuples[-1][2]
    assert not validator2(2)
    expected_number_of_log += 1
    assert len(caplog.record_tuples) == expected_number_of_log
    assert 'x must be smaller than 1' in caplog.record_tuples[-1][2]

    # case 3: multiple validators and multiple error messages
    validator3 = integrate_validators(
        is_valid=(
            partial(x_is_smaller_than_y, y=2),
            partial(x_is_smaller_than_y, y=1),
        ),
        error_message=(
            'x must be smaller than 2',
            'x must be smaller than 1',
        ),
    )
    # valid
    assert validator3(0)
    assert len(caplog.record_tuples) == expected_number_of_log
    # invalid
    assert not validator3(1)
    expected_number_of_log += 1
    assert len(caplog.record_tuples) == expected_number_of_log
    assert 'x must be smaller than 1' in caplog.record_tuples[-1][2]
    assert not validator3(2)
    expected_number_of_log += 1
    assert len(caplog.record_tuples) == expected_number_of_log
    assert 'x must be smaller than 2' in caplog.record_tuples[-1][2]


@pytest.mark.sdk
def test_integrate_validators_error():

    with pytest.raises(ValueError):
        integrate_validators(
            is_valid=[],
            error_message='x must be smaller than 1',
        )

    with pytest.raises(ValueError):
        integrate_validators(
            is_valid=lambda x: x < 1,
            error_message=[],
        )

    with pytest.raises(ValueError):
        integrate_validators(
            is_valid=lambda x: x < 1,
            error_message=['x must be smaller than 1', 'x must be smaller than 2'],  # noqa
        )
