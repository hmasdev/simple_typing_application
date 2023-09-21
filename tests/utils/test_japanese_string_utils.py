from functools import partial

import pytest
import requests
from requests import Response
from simple_typing_application.utils.japanese_string_utils import (
    is_hiragana,
    delete_space_between_hiraganas,
    excelapi_kanji2kana,
)
from simple_typing_application.utils.rerun import MaxRetryError


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


@pytest.mark.parametrize(
    "input_text,transform_katakana_to_hiragana,expected",
    [
        ("これは日本語デス。", True, "これはにほんごです。"),
        ("これは日本語デス。", False, "これはにほんごデス。"),
    ],
)
def test_excelapi_kanji2kana(
    input_text: str,
    transform_katakana_to_hiragana: bool,
    expected: str,
    mocker
):

    # mock
    mock_response = mocker.MagicMock(spec=Response)
    mock_response.text = expected
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mocker.patch(
        "simple_typing_application.utils.japanese_string_utils.requests.get",
        return_value=mock_response,
    )

    # execute
    actual: str = excelapi_kanji2kana(
        input_text,
        transform_katakana_to_hiragana=transform_katakana_to_hiragana
    )

    # assert
    assert actual == expected


def test_excelapi_kanji2kana_request_get_raises_1error(mocker):

    # preparation
    input_text: str = "これは日本語デス。"
    expected: str = "これはにほんごです。"
    ctr: int = 0

    # mock
    def mock_requests_get(*args, **kwargs):
        nonlocal ctr
        nonlocal mock_response  # type: ignore
        ctr += 1
        if ctr == 1:
            raise requests.exceptions.RequestException()
        else:
            return mock_response

    mock_response = mocker.MagicMock(spec=Response)
    mock_response.text = expected
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_request_get = mocker.patch(
        "simple_typing_application.utils.japanese_string_utils.requests.get",
        side_effect=mock_requests_get,
    )

    # execute
    actual: str = excelapi_kanji2kana(input_text)

    # assert
    assert ctr == 2  # 1st: raise, 2nd: success
    assert mock_request_get.call_count == 2
    assert actual == expected


def test_excelapi_kanji2kana_request_get_raises_error_always(mocker):

    # preparation
    input_text: str = "これは日本語です。"
    max_retry: int = 3

    # mock
    mock_request_get = mocker.patch(
        "simple_typing_application.utils.japanese_string_utils.requests.get",
        side_effect=requests.exceptions.RequestException,
    )

    # execute
    with pytest.raises(MaxRetryError):
        excelapi_kanji2kana(input_text, interval_sec=0.1, max_retry=max_retry)  # noqa
    assert mock_request_get.call_count == max_retry


@pytest.mark.parametrize(
    'status_code',
    [
        400,
        500,
    ],
)
def test_excelapi_kanji2kana_invalid_status_code(
    status_code: int,
    mocker,
):
    # preparation
    input_text: str = "これは日本語です。"

    # mock
    mock_response = mocker.MagicMock(spec=Response)
    mock_response.status_code = status_code
    mock_response.reason = "test reason"
    mock_response.url = "test url"
    mock_response.raise_for_status = partial(Response.raise_for_status, mock_response)  # noqa
    mocker.patch(
        "simple_typing_application.utils.japanese_string_utils.requests.get",
        return_value=mock_response,
    )

    # execute
    with pytest.raises(requests.exceptions.HTTPError):
        excelapi_kanji2kana(input_text)


@pytest.mark.integrate
def test_excelapi_kanji2kana_integrate(mocker):

    # preparation
    input_text: str = "これは日本語デス。ABC abc"
    expected: str = "これはにほんごです。ABC abc"

    # execute
    actual: str = excelapi_kanji2kana(
        input_text,
        transform_katakana_to_hiragana=True,
    )

    # assert
    assert actual == expected
