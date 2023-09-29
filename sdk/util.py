from functools import wraps
from logging import getLogger, Logger
from typing import Any, Callable, Collection


def input_until_valid(
    prompt: str,
    is_valid: Callable[[str], bool] | None = None,
    callback: Callable[[str], Any] | None = None,
    logger: Logger = getLogger(__name__),
) -> str | Any:
    while True:
        # Get input
        input_ = input(prompt)
        logger.debug(f"Input: '{input_}'")
        # Validate
        if is_valid is None or is_valid(input_):
            # Return
            if callback is not None:
                return callback(input_)
            else:
                return input_
        # Validation failed
        logger.error(f"Invalid input: '{input_}'. Try again.")


def error_detection_validator_deco(
    func: Callable[[Any], Any],
    logger: Logger = getLogger(__name__),
) -> Callable[[Any], bool]:  # noqa
    @wraps(func)
    def validator(x: Any) -> bool:
        try:
            func(x)
            return True
        except Exception as e:
            logger.error(f'Error detected: {e}')
            return False
    return validator


def integrate_validators(
    is_valid: Callable[[Any], bool] | Collection[Callable[[Any], bool]],
    error_message: str | Collection[str] = 'Validation failed.',
    logger: Logger = getLogger(__name__),
) -> Callable[[Any], bool]:

    # preparation
    if callable(is_valid):
        is_valid = (is_valid,)
    if isinstance(error_message, str):
        error_message = [error_message for _ in range(len(is_valid))]
    # validation
    if len(is_valid) == 0:
        raise ValueError('is_valid must not be empty.')
    if len(error_message) == 0:
        raise ValueError('error_message must not be empty.')
    if len(is_valid) != len(error_message):
        raise ValueError('The number of error_message must be 1 or equal to the number of is_valid')  # noqa

    # integrate is_valid
    def validator(x: Any) -> bool:
        for v, e in zip(is_valid, error_message):
            if not v(x):
                logger.error(f'For the inout {x}, the following message has been caught: {e}')  # noqa
                return False
        return True
    return validator
