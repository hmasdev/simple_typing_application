import logging
import time
from functools import wraps, partial
from logging import Logger, getLogger
from typing import Callable, TypeVar, ParamSpec

T = TypeVar("T")
P = ParamSpec("P")

logger: Logger = getLogger(__name__)


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
        logger (Logger, optional): logger. Defaults to logger.

    Returns:
        Callable[P, T]: decorated function.

    Note:
        If func is None, return a decorator. Otherwise, return a wrapper.
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

    # if func is None, return a decorator
    if func is None:
        return partial(
            stopwatch_deco,
            logger=logger,
        )

    # preparation
    if hasattr(func, "__name__"):
        funcname = func.__name__
    else:
        funcname = str(func)

    if prefix is None:
        prefix = f"Execution time of {funcname}()"

    log_msg_fmt: str = f"{prefix}: {{elapsed_time:.6f}} seconds{postfix}"

    log_func = {
        logging.DEBUG: logger.debug,
        logging.INFO: logger.info,
        logging.WARNING: logger.warning,
        logging.ERROR: logger.error,
        logging.CRITICAL: logger.critical,
    }[level]

    # if func is not None, return a wrapper
    @wraps(func)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            log_func(log_msg_fmt.format(elapsed_time=end_time - start_time))
        return result

    return wrapped
