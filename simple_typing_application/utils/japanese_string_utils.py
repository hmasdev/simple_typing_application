import requests
import time

from ..const.hiragana_katakana_map import KATAKANA2HIRAGANA_MAP
from .rerun import rerun_deco


def is_hiragana(c: str) -> bool:
    """Check if a character is a hiragana.

    Args:
        c (str): a character.

    Returns:
        bool: True if a character is a hiragana, otherwise False.

    Raises:
        ValueError: if len(c) != 1.

    Examples:
    >>> is_hiragana('あ')
    True
    >>> is_hiragana('ア')
    False
    >>> is_hiragana('a')
    False
    """
    if len(c) != 1:
        raise ValueError(f"len(c) must be 1, but {len(c)}")
    return "ぁ" <= c <= "ゔ"


def delete_space_between_hiraganas(s: str) -> str:
    """Delete spaces between hiraganas.

    Args:
        s (str): a string of hiraganas and spaces.

    Returns:
        str: a string of hiraganas without spaces.

    Examples:
    >>> s = 'こ んに ち は'
    >>> delete_space_between_hiraganas(s)
    'こんにちは'
    """
    if len(s) <= 2:
        return s
    return (
        s[:1]
        + "".join(
            [
                b
                for a, b, c in zip(s[:-2], s[1:-1], s[2:])
                if not (is_hiragana(a) and is_hiragana(c) and b in [" ", "　"])
            ]
        )
        + s[-1:]
    )


def excelapi_kanji2kana(
    text: str,
    transform_katakana_to_hiragana: bool = True,
    max_retry: int = 3,
    interval_sec: float = 3.0,
) -> str:
    """Convert kanji to kana using excelapi.org.

    Args:
        text (str): a string including kanji.
        transform_katakana_to_hiragana (bool, optional): if True, transform katakana to hiragana. Defaults to True.
        max_retry (int, optional): max number of retries. Defaults to 3.
        interval_sec (float, optional): interval seconds between retries. Defaults to 3.

    Returns:
        str: a string including kana.

    Raises:
        requests.exceptions.HTTPError: if the status code is not 20x.
        simple_typing_application.utils.rerun.MaxRetryError: if requests.get fails max_retry times.

    NOTE:
        ref. https://excelapi.org/docs/language/kanji2kana/
    """  # noqa

    url = f"https://api.excelapi.org/language/kanji2kana?text={text}"
    response = rerun_deco(
        requests.get,
        max_retry=max_retry,
        callback=lambda *args, **kwargs: time.sleep(interval_sec),
    )(url)

    # chech status code
    response.raise_for_status()
    transformed_text: str = response.text

    # katakana -> hiragana
    if transform_katakana_to_hiragana:
        for k, h in KATAKANA2HIRAGANA_MAP.items():
            transformed_text = transformed_text.replace(k, h)

    return transformed_text
