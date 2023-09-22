import pytest

from simple_typing_application.models.config_model import (
    ESentenceGeneratorType,
    BaseSentenceGeneratorConfigModel,
    OpenAISentenceGeneratorConfigModel,
    HuggingfaceSentenceGeneratorConfigModel,
    StaticSentenceGeneratorConfigModel,
)
from simple_typing_application.sentence_generator.factory import create_sentence_generator  # noqa
from simple_typing_application.sentence_generator.huggingface_sentence_generator import HuggingfaceSentenceGenerator  # noqa
from simple_typing_application.sentence_generator.openai_sentence_generator import OpenaiSentenceGenerator  # noqa
from simple_typing_application.sentence_generator.static_sentence_generator import StaticSentenceGenerator  # noqa


@pytest.mark.parametrize(
    "sentence_generator_type, sentence_generator_config, expected_class",
    [
        (
            ESentenceGeneratorType.OPENAI,
            OpenAISentenceGeneratorConfigModel(),
            OpenaiSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.HUGGINGFACE,
            HuggingfaceSentenceGeneratorConfigModel(),
            HuggingfaceSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.STATIC,
            StaticSentenceGeneratorConfigModel(text_kana_map={}),
            StaticSentenceGenerator,
        ),
    ]
)
def test_create_sentence_generator(
    sentence_generator_type: ESentenceGeneratorType,
    sentence_generator_config: BaseSentenceGeneratorConfigModel,
    expected_class: type,
    mocker,
):

    # mock
    # for OpenaiSentenceGenerator
    mocker.patch('simple_typing_application.sentence_generator.openai_sentence_generator.ChatOpenAI')  # noqa
    mocker.patch('simple_typing_application.sentence_generator.openai_sentence_generator.ConversationChain')  # noqa
    mocker.patch('simple_typing_application.sentence_generator.openai_sentence_generator.ConversationBufferMemory')  # noqa
    # for HuggingfaceSentenceGenerator
    mocker.patch('simple_typing_application.sentence_generator.huggingface_sentence_generator.AutoModelForCausalLM.from_pretrained')  # noqa
    mocker.patch('simple_typing_application.sentence_generator.huggingface_sentence_generator.AutoTokenizer.from_pretrained')  # noqa
    mocker.patch('simple_typing_application.sentence_generator.huggingface_sentence_generator.pipeline')  # noqa
    # for StaticSentenceGenerator
    # None

    # execute
    sentence_generator = create_sentence_generator(
        sentence_generator_type,
        sentence_generator_config,
    )

    # assert
    assert isinstance(sentence_generator, expected_class)
