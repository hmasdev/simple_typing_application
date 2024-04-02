import asyncio
import logging
import pytest

try:
    import torch  # type: ignore # noqa
    import transformers  # type: ignore # noqa
    HUGGINGFACE_SETUP = True
except ImportError:
    HUGGINGFACE_SETUP = False

from simple_typing_application.models.typing_target_model import TypingTargetModel  # noqa
from simple_typing_application.sentence_generator.base import BaseSentenceGenerator  # noqa
from simple_typing_application.sentence_generator.huggingface_sentence_generator import HuggingfaceSentenceGenerator  # noqa


@pytest.mark.skipif(
    not HUGGINGFACE_SETUP,
    reason='Libs for HuggingfaceSentenceGenerator like torch is not installed.',  # noqa
)
def test_inheritance():
    assert issubclass(HuggingfaceSentenceGenerator, BaseSentenceGenerator)


@pytest.mark.skipif(
    not HUGGINGFACE_SETUP,
    reason='Libs for HuggingfaceSentenceGenerator like torch is not installed.',  # noqa
)
def test_generate(mocker):

    # preparation
    expected = TypingTargetModel(
        text="text これはサンプルの文章です。",
        text_hiragana_alphabet_symbol="text これはさんぷるのぶんしょうです。",
        typing_target=[
            ["t"], ["e"], ["x"], ["t"], [" "],
            ['ko', 'co'],
            ['re'],
            ['ha'],
            ['sa'],
            ["nnpu", "n'pu", "xnpu", "npu"],
            ['ru'],
            ['no'],
            ['bu'],
            [
                "nnsyo", "n'syo", "xnsyo", "nsyo",
                "nnsho", "n'sho", "xnsho", "nsho",
                "nnsixyo", "n'sixyo", "xnsixyo", "nsixyo",
                "nnsilyo", "n'silyo", "xnsilyo", "nsilyo",
                "nnshixyo", "n'shixyo", "xnshixyo", "nshixyo",
                "nnshilyo", "n'shilyo", "xnshilyo", "nshilyo",
                "nncixyo", "n'cixyo", "xncixyo", "ncixyo",
                "nncilyo", "n'cilyo", "xncilyo", "ncilyo",
            ],
            ['u', 'wu', "whu"],
            ['de'],
            ['su'],
            ['.'],
        ]
    )

    # mock
    mocker.patch('simple_typing_application.sentence_generator.huggingface_sentence_generator.AutoModelForCausalLM')  # noqa
    mocker.patch('simple_typing_application.sentence_generator.huggingface_sentence_generator.AutoTokenizer')  # noqa
    mock_generator = mocker.MagicMock(return_value=[{"generated_text": expected.text}])  # noqa
    mocker.patch(
        'simple_typing_application.sentence_generator.huggingface_sentence_generator.pipeline',  # noqa
        return_value=mock_generator,
    )
    mocker.patch(
        'simple_typing_application.sentence_generator.huggingface_sentence_generator.excelapi_kanji2kana',  # noqa
        return_value=expected.text_hiragana_alphabet_symbol,
    )

    # execute
    actual = asyncio.run(HuggingfaceSentenceGenerator().generate())

    # sort the list of list
    # NOTE: the order of the list of list is not important.
    expected.typing_target = [sorted(x) for x in expected.typing_target]
    actual.typing_target = [sorted(x) for x in actual.typing_target]

    # assert
    assert actual == expected


@pytest.mark.skipif(
    not HUGGINGFACE_SETUP,
    reason='Libs for HuggingfaceSentenceGenerator like torch is not installed.',  # noqa
)
@pytest.mark.integrate
def test_generate_integrate():
    # execute
    actual = asyncio.run(HuggingfaceSentenceGenerator().generate())
    logging.info(f'generated: {actual}')
    if len(actual.text) < 5:
        logging.warning(f'generated text may be too small: {actual.text}')

    # TODO: assert
