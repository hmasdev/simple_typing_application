from __future__ import annotations
import asyncio
from functools import partial, wraps
from logging import Logger, getLogger
from typing import Any, Callable


class MaxRetryError(Exception):
    def __init__(self, message: str = ''):
        super().__init__(message)


def rerun_deco(
    func: Callable[..., Any] | None = None,
    max_retry: int = 5,
    callback: Callable[..., None] | None = None,
    logger: Logger = getLogger(__name__),
) -> Callable[..., Any]:
    '''Decorator to rerun a function when it raises an exception.

    Args:
        func (Callable[..., Any], optional): function to be decorated. Defaults to None.
        max_retry (int, optional): max retry count. Defaults to 5.
        callback (Callable[..., None], optional): callback function to be called when func raises an exception. Defaults to None.
        logger (Logger, optional): logger. Defaults to getLogger(__name__).

    Raises:
        MaxRetryError: raised when func raises an exception max_retry times.

    Returns:
        Callable[..., Any]: decorated function.

    Note:
        If func is None, return a decorator. Otherwise, return a wrapper.
    '''  # noqa

    # if func is None, return a decorator
    if func is None:
        return partial(
            rerun_deco,
            max_retry=max_retry,
            callback=callback,
            logger=logger,
        )

    # if func is not None, return a wrapper
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            for i in range(max_retry):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if hasattr(func, '__name__'):
                        logger.warning(f'[{i+1}/{max_retry}] failed to run {func.__name__}(): {e.__class__.__name__}({e})')  # noqa
                    else:
                        logger.warning(f'[{i+1}/{max_retry}] failed to run an unnamed function: {e.__class__.__name__}({e})')  # noqa
                    if callback is not None:
                        callback(*args, **kwargs)
            raise MaxRetryError()
    else:
        @wraps(func)
        def wrapped(*args, **kwargs):
            for i in range(max_retry):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if hasattr(func, '__name__'):
                        logger.warning(f'failed to run {func.__name__}(): {e.__class__.__name__}({e})')  # noqa
                    else:
                        logger.warning(f'failed to run an unnamed function: {e.__class__.__name__}({e})')  # noqa
                    if callback is not None:
                        callback(*args, **kwargs)
            raise MaxRetryError()

    return wrapped
