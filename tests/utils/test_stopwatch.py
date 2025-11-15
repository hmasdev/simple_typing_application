import logging
import re

import pytest

from simple_typing_application.utils.stopwatch import stopwatch_deco


def _get_latest_record(caplog):
    assert caplog.records, "Expected logger to emit at least one record"
    return caplog.records[-1]


def test_stopwatch_logs_with_default_prefix(caplog):
    """Decorator without args should log INFO with default prefix."""

    caplog.set_level(logging.INFO, logger="simple_typing_application.utils.stopwatch")

    @stopwatch_deco
    def add(a: int, b: int) -> int:
        return a + b

    assert add(1, 2) == 3
    record = _get_latest_record(caplog)
    assert record.levelno == logging.INFO
    assert record.message.startswith("Execution time of add()")
    assert record.message.endswith(" seconds")
    assert re.match(r"Execution time of add\(\): \d+\.\d{6} seconds", record.message)


def test_stopwatch_logs_when_called_with_parentheses(caplog):
    """Calling stopwatch_deco() triggers the func is None branch and still logs."""

    caplog.set_level(logging.INFO, logger="simple_typing_application.utils.stopwatch")

    @stopwatch_deco()
    def greet() -> str:
        return "hello"

    assert greet() == "hello"
    record = _get_latest_record(caplog)
    assert "Execution time of greet()" in record.message


def test_stopwatch_custom_prefix_postfix_and_level(caplog):
    """Manually decorating allows passing custom prefix/postfix/level and logger."""

    custom_logger = logging.getLogger("tests.utils.stopwatch.custom")
    caplog.set_level(logging.ERROR, logger=custom_logger.name)

    def sample() -> None:
        return None

    wrapped = stopwatch_deco(
        sample,
        prefix="Run sample",
        postfix=" !!!",
        level=logging.ERROR,
        logger=custom_logger,
    )

    wrapped()
    record = _get_latest_record(caplog)
    assert record.levelno == logging.ERROR
    assert record.message.startswith("Run sample: ")
    assert record.message.endswith(" seconds !!!")


def test_stopwatch_invalid_level_raises_value_error():
    with pytest.raises(ValueError):
        stopwatch_deco(level=123)
