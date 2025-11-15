import logging
import time
from contextlib import contextmanager
from functools import wraps, partial
from logging import Logger, getLogger
from typing import Callable, Generator, TypeVar, ParamSpec

T = TypeVar("T")
P = ParamSpec("P")

logger: Logger = getLogger(__name__)


@contextmanager
def stopwatch(
    level: int = logging.INFO,
    prefix: str | None = None,
    postfix: str = "",
    logger: Logger = logger,
) -> Generator[None, None, None]:
    """Context manager to measure the execution time of a code block.

    Args:
        level (int, optional): log level. Defaults to logging.INFO.
            Must be one of logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL.
        prefix (str | None, optional): prefix of the log message. Defaults to None.
        postfix (str, optional): postfix of the log message. Defaults to "".
        logger (Logger, optional): logger. Defaults to logger.

    Yields:
        None: None
    """  # noqa

    # validation
    if level not in {
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    }:
        raise ValueError(
            f"Invalid log level: {level}. "
            "Must be one of logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL.",  # noqa
        )

    # preparation
    if prefix is None:
        prefix = "Execution time"

    log_msg_fmt: str = f"{prefix}: {{elapsed_time:.6f}} seconds{postfix}"

    log_func = {
        logging.DEBUG: logger.debug,
        logging.INFO: logger.info,
        logging.WARNING: logger.warning,
        logging.ERROR: logger.error,
        logging.CRITICAL: logger.critical,
    }[level]

    # execution
    start_time = time.perf_counter()
    try:
        yield
    finally:
        end_time = time.perf_counter()
        log_func(log_msg_fmt.format(elapsed_time=end_time - start_time))


def stopwatch_deco(
    func: Callable[P, T] | None = None,
    *,
    level: int = logging.INFO,
    prefix: str | None = None,
    postfix: str = "",
    logger: Logger = logger,
) -> Callable[P, T]:
    """Decorator to measure the execution time of a function.

    Args:
        func (Callable[P, T], optional): function to be decorated. Defaults to None.
        *,
        level (int, optional): log level. Defaults to logging.INFO.
            Must be one of logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL.
        prefix (str | None, optional): prefix of the log message. Defaults to None.
        postfix (str, optional): postfix of the log message. Defaults to "".
        logger (Logger, optional): logger. Defaults to logger.

    Returns:
        Callable[P, T]: decorated function.

    Note:
        If func is None, return a decorator. Otherwise, return a wrapper.
    """  # noqa

    # if func is None, return a decorator
    if func is None:
        return partial(
            stopwatch_deco,
            level=level,
            prefix=prefix,
            postfix=postfix,
            logger=logger,
        )

    if prefix is None:
        prefix = f"Execution time of {getattr(func, '__name__', str(func))}"

    # if func is not None, return a wrapper
    @wraps(func)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        with stopwatch(
            level=level,
            prefix=prefix,
            postfix=postfix,
            logger=logger,
        ):
            result = func(*args, **kwargs)
        return result

    return wrapped
