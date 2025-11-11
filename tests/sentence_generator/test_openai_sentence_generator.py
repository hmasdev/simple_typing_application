import asyncio
import os
import pytest
from simple_typing_application.models.typing_target_model import TypingTargetModel  # noqa
from simple_typing_application.sentence_generator.base import BaseSentenceGenerator  # noqa
from simple_typing_application.sentence_generator.openai_sentence_generator import (  # noqa
    _OutputSchema,
    OpenaiSentenceGenerator,
)


def test_inheritance():
    assert issubclass(OpenaiSentenceGenerator, BaseSentenceGenerator)


def test__OutputSchema_build_typing_target():

    # preparation
    output_schema = _OutputSchema(
        text="text これはサンプルの文章です。",
        text_hiragana_alphabet_symbol="text これはさんぷるのぶんしょうです。",
    )
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

    # execute
    actual = output_schema.build_typing_target()

    # sort the list of list
    # NOTE: the order of the list of list is not important.
    expected.typing_target = [sorted(x) for x in expected.typing_target]
    actual.typing_target = [sorted(x) for x in actual.typing_target]

    # assert
    assert actual == expected


def test_generate(mocker):

    # preparation
    mocker.patch(
        "simple_typing_application.sentence_generator.openai_sentence_generator.ChatOpenAI",  # noqa
        autospec=True,
    )
    mocker.patch(
        "simple_typing_application.sentence_generator.openai_sentence_generator.create_agent",  # noqa
        autospec=True,
        return_value=mocker.Mock(),
    )
    sentence_generator = OpenaiSentenceGenerator()
    sentence_generator._agent = mocker.Mock()
    sentence_generator._agent.ainvoke = mocker.AsyncMock(return_value={
        "structured_response": _OutputSchema(
            text="text これはサンプルの文章です。",
            text_hiragana_alphabet_symbol="text これはさんぷるのぶんしょうです。",
        )
    })

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

    # execute
    actual = asyncio.run(sentence_generator.generate())

    # sort the list of list
    # NOTE: the order of the list of list is not important.
    expected.typing_target = [sorted(x) for x in expected.typing_target]
    actual.typing_target = [sorted(x) for x in actual.typing_target]

    # assert
    assert actual == expected


@pytest.mark.integrate
@pytest.mark.skipif(
    os.getenv('OPENAI_API_KEY') is None,
    reason='Environment variable "OPENAI_API_KEY" is not set.'
)
def test_generate_integrate():
    # execute
    asyncio.run(OpenaiSentenceGenerator().generate())
    # TODO: assert
