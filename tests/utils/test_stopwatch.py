import logging
import re

import pytest

from simple_typing_application.utils.stopwatch import stopwatch, stopwatch_deco


LOGGER_NAME = "simple_typing_application.utils.stopwatch"


def _latest_record(caplog):
    assert caplog.records, "Expected stopwatch to emit a log record"
    return caplog.records[-1]


def test_stopwatch_context_manager_logs_default_prefix(caplog):
    caplog.set_level(logging.INFO, logger=LOGGER_NAME)

    with stopwatch():
        sum(range(5))

    record = _latest_record(caplog)
    assert record.levelno == logging.INFO
    assert re.match(r"Execution time: \d+\.\d{6} seconds", record.message)


def test_stopwatch_context_manager_custom_prefix_postfix_and_level(caplog):
    custom_logger = logging.getLogger("tests.utils.stopwatch.ctx")
    caplog.set_level(logging.WARNING, logger=custom_logger.name)

    with stopwatch(
        level=logging.WARNING,
        prefix="Block",
        postfix=" !!!",
        logger=custom_logger,
    ):
        sum(range(10))

    record = _latest_record(caplog)
    assert record.levelno == logging.WARNING
    assert record.message.startswith("Block: ")
    assert record.message.endswith(" seconds !!!")


def test_stopwatch_context_manager_invalid_level_raises_value_error():
    with pytest.raises(ValueError):
        with stopwatch(level=123):
            pass


def test_stopwatch_decorator_without_parentheses_uses_func_name_in_prefix(caplog):
    caplog.set_level(logging.INFO, logger=LOGGER_NAME)

    @stopwatch_deco
    def greet(name: str) -> str:
        return f"hello {name}"

    assert greet("world") == "hello world"
    record = _latest_record(caplog)
    assert record.levelno == logging.INFO
    assert re.match(r"Execution time of greet: \d+\.\d{6} seconds", record.message)


def test_stopwatch_decorator_called_with_parentheses(caplog):
    caplog.set_level(logging.INFO, logger=LOGGER_NAME)

    @stopwatch_deco()
    def add(a: int, b: int) -> int:
        return a + b

    assert add(1, 2) == 3
    record = _latest_record(caplog)
    assert re.match(r"Execution time of add: \d+\.\d{6} seconds", record.message)


def test_stopwatch_decorator_custom_prefix_and_invalid_level(caplog):
    caplog.set_level(logging.ERROR, logger=LOGGER_NAME)

    @stopwatch_deco(
        prefix="Manual",
        postfix=" !!!",
        level=logging.ERROR,
    )
    def work() -> None:
        return None

    work()

    record = _latest_record(caplog)
    assert record.levelno == logging.ERROR
    assert record.message.startswith("Manual: ")
    assert record.message.endswith(" seconds !!!")

    @stopwatch_deco(level=123)
    def broken():
        return None

    with pytest.raises(ValueError):
        broken()
