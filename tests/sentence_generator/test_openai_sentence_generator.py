import asyncio
import os
from unittest.mock import AsyncMock
import pytest
from simple_typing_application.models.typing_target_model import TypingTargetModel  # noqa
from simple_typing_application.sentence_generator.base import BaseSentenceGenerator  # noqa
from simple_typing_application.sentence_generator.openai_sentence_generator import OpenaiSentenceGenerator  # noqa


def test_inheritance():
    assert issubclass(OpenaiSentenceGenerator, BaseSentenceGenerator)


def test_clean(mocker):

    # mock
    mocker.patch('simple_typing_application.sentence_generator.openai_sentence_generator.ChatOpenAI')  # noqa
    mocker.patch('simple_typing_application.sentence_generator.openai_sentence_generator.ConversationBufferMemory')  # noqa
    mocker.patch('simple_typing_application.sentence_generator.openai_sentence_generator.ConversationChain')  # noqa

    # preparation
    s = """以下が出力です。

```json
{
    "text": "text これはサンプルの文章です。",
    "text_hiragana_alphabet_symbol": "text これはさんぷるのぶんしょうです。"
}
```
"""
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
    actual = OpenaiSentenceGenerator().clean(s)

    # sort the list of list
    # NOTE: the order of the list of list is not important.
    expected.typing_target = [sorted(x) for x in expected.typing_target]
    actual.typing_target = [sorted(x) for x in actual.typing_target]

    # assert
    assert actual == expected


def test_generate(mocker):

    # mock
    mocker.patch('simple_typing_application.sentence_generator.openai_sentence_generator.ChatOpenAI')  # noqa
    mocker.patch('simple_typing_application.sentence_generator.openai_sentence_generator.ConversationBufferMemory')  # noqa
    mock_chain = mocker.patch('simple_typing_application.sentence_generator.openai_sentence_generator.ConversationChain', new=AsyncMock)  # noqa
    mock_chain.arun = AsyncMock(return_value="""以下が出力です。

```json
{
    "text": "text これはサンプルの文章です。",
    "text_hiragana_alphabet_symbol": "text これはさんぷるのぶんしょうです。"
}
```
""")

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

    # execute
    actual = asyncio.run(OpenaiSentenceGenerator().generate())

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
