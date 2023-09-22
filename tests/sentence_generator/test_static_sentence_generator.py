import asyncio
import random

import pytest
from simple_typing_application.models.typing_target_model import TypingTargetModel  # noqa
from simple_typing_application.sentence_generator.base import BaseSentenceGenerator  # noqa
from simple_typing_application.sentence_generator.static_sentence_generator import StaticSentenceGenerator  # noqa


TUP_TYPING_TARGET: tuple[TypingTargetModel, ...] = (
    TypingTargetModel(
        text='Hello, 世界！',
        text_hiragana_alphabet_symbol='Hello、せかい！',
        typing_target=list(map(sorted, [['H'], ['e'], ['l'], ['l'], ['o'], [','], ['se', 'ce'], ['ka', 'ca'], ['i', 'yi'], ['!']])),    # type: ignore # noqa
    ),
    TypingTargetModel(
        text='ファーブル',
        text_hiragana_alphabet_symbol='ふぁーぶる',
        typing_target=list(map(sorted, [['fa', 'huxa', 'hula', 'fuxa', 'fula'], ['-'], ['bu'], ['ru']])),    # type: ignore # noqa
    ),
)


def test_inhertance():
    assert issubclass(StaticSentenceGenerator, BaseSentenceGenerator)


@pytest.mark.parametrize(
    "is_random, state, expecteds",
    [
        (
            False,
            random.getstate(),
            [
                (
                    TUP_TYPING_TARGET[idx % len(TUP_TYPING_TARGET)].text,
                    TUP_TYPING_TARGET[idx % len(TUP_TYPING_TARGET)].text_hiragana_alphabet_symbol,  # noqa
                )
                for idx in range(5 * len(TUP_TYPING_TARGET))
            ],
        ),
        (
            True,
            random.getstate(),
            [
                tuple(
                    v
                    for k, v in TUP_TYPING_TARGET[random.randint(0, len(TUP_TYPING_TARGET) - 1)].model_dump().items()  # noqa
                    if k in [
                        'text',
                        'text_hiragana_alphabet_symbol',
                    ]
                )
                for _ in range(5 * len(TUP_TYPING_TARGET))
            ],
        ),
    ]
)
def test__get_next(
    is_random: bool,
    state: tuple,
    expecteds: list[tuple[str, str]],
    mocker
):

    # mock
    mock_excelapi_kanji2kana = mocker.patch(
        'simple_typing_application.sentence_generator.static_sentence_generator.excelapi_kanji2kana',  # noqa
        side_effect={
            t.text: t.text_hiragana_alphabet_symbol
            for t in TUP_TYPING_TARGET
        }.get,
    )

    # preparation
    num_calls: int = len(expecteds)
    generator = StaticSentenceGenerator(
        text_kana_map={
            target.text: None
            for target in TUP_TYPING_TARGET
        },
        is_random=is_random,
    )
    # NOTE: to check whether _get_next generates targets cyclically  # noqa
    assert num_calls > len(TUP_TYPING_TARGET)

    # execute
    random.setstate(state)
    actuals = [generator._get_next() for _ in range(num_calls)]

    # assert
    assert mock_excelapi_kanji2kana.call_count == len(TUP_TYPING_TARGET)
    assert actuals == expecteds


@pytest.mark.parametrize(
    "is_random, state, expecteds",
    [
        (
            False,
            random.getstate(),
            [
                TUP_TYPING_TARGET[idx % len(TUP_TYPING_TARGET)]
                for idx in range(5 * len(TUP_TYPING_TARGET))
            ],
        ),
        (
            True,
            random.getstate(),
            [
                TUP_TYPING_TARGET[random.randint(0, len(TUP_TYPING_TARGET) - 1)]  # noqa
                for _ in range(5 * len(TUP_TYPING_TARGET))
            ],
        ),
    ]
)
def test_generate(
    is_random: bool,
    state: tuple,
    expecteds: list[TypingTargetModel],
    mocker
):

    # mock
    mock_excelapi_kanji2kana = mocker.patch(
        'simple_typing_application.sentence_generator.static_sentence_generator.excelapi_kanji2kana',  # noqa
        side_effect={
            t.text: t.text_hiragana_alphabet_symbol
            for t in TUP_TYPING_TARGET
        }.get,
    )

    # preparation
    num_calls: int = len(expecteds)
    generator = StaticSentenceGenerator(
        text_kana_map={
            target.text: None
            for target in TUP_TYPING_TARGET
        },
        is_random=is_random,
    )
    # NOTE: to check whether _get_next generates targets cyclically  # noqa
    assert num_calls > len(TUP_TYPING_TARGET)

    # execute
    random.setstate(state)
    actuals = [asyncio.run(generator.generate()) for _ in range(num_calls)]
    # NOTE: the order of typing_target is not important
    for actual in actuals:
        actual.typing_target = list(map(sorted, actual.typing_target))  # type: ignore  # noqa

    # assert
    assert mock_excelapi_kanji2kana.call_count == len(TUP_TYPING_TARGET)
    assert actuals == expecteds
