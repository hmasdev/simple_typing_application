import pytest
from simple_typing_application.utils.japanese_string_utils import (
    is_hiragana,
    delete_space_between_hiraganas
)


@pytest.mark.parametrize(
    "c,expected",
    [
        ("ぁ", True),
        ("あ", True),
        ("い", True),
        ("ゔ", True),
        (chr(ord('ぁ')-1), False),
        (chr(ord('ゔ')+1), False),
        ("ア", False),
        ("a", False),
        (")", False),
    ],
)
def test_is_hiragana(
    c: str,
    expected: bool,
):
    actual: bool = is_hiragana(c)
    assert actual == expected


def test_is_hiragana_raise_error():
    with pytest.raises(ValueError):
        is_hiragana("aa")


@pytest.mark.parametrize(
    "s,expected",
    [
        ("こ んに ち は ", "こんにちは "),  # Hankaku space
        ("こ　んに ち は　", "こんにちは　"),  # Zenkaku space
        ("This is a pen.", "This is a pen."),  # Alphabet case
        ("これ は ab です。", "これは ab です。"),  # mixed case
        ("", ""),  # empty string
        ("こ", "こ"),  # single hiragana
        ("こ ん", "こん"),  # single hiragana with space
    ],
)
def test_delete_space_between_hiraganas(
    s: str,
    expected: str,
):
    actual: str = delete_space_between_hiraganas(s)
    assert actual == expected
