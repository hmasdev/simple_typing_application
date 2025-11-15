from __future__ import annotations
import pytest

try:
    import torch  # type: ignore # noqa
    import accelerate  # type: ignore # noqa
    import protobuf  # type: ignore # noqa
    import transformers  # type: ignore # noqa
    import sentencepiece  # type: ignore # noqa

    HUGGINGFACE_SETUP = True
except ImportError:
    HUGGINGFACE_SETUP = False

from simple_typing_application.const.sentence_generator import ESentenceGeneratorType  # noqa
from simple_typing_application.models.config_models.sentence_generator_config_model import (  # noqa
    BaseSentenceGeneratorConfigModel,
    HuggingfaceSentenceGeneratorConfigModel,
    OpenAISentenceGeneratorConfigModel,
    StaticSentenceGeneratorConfigModel,
)
from simple_typing_application.sentence_generator.factory import (
    create_sentence_generator,
    _select_class_and_config_model,
)
from simple_typing_application.sentence_generator.huggingface_sentence_generator import HuggingfaceSentenceGenerator  # noqa
from simple_typing_application.sentence_generator.openai_sentence_generator import OpenaiSentenceGenerator  # noqa
from simple_typing_application.sentence_generator.static_sentence_generator import StaticSentenceGenerator  # noqa


@pytest.mark.parametrize(
    "sentence_generator_type, expected_class, expected_config_model",
    [
        (
            ESentenceGeneratorType.OPENAI,
            OpenaiSentenceGenerator,
            OpenAISentenceGeneratorConfigModel,
        ),
        (
            ESentenceGeneratorType.HUGGINGFACE,
            HuggingfaceSentenceGenerator,
            HuggingfaceSentenceGeneratorConfigModel,
        ),
        (
            ESentenceGeneratorType.STATIC,
            StaticSentenceGenerator,
            StaticSentenceGeneratorConfigModel,
        ),
    ],
)
def test_select_class_and_config_model(
    sentence_generator_type: ESentenceGeneratorType,
    expected_class: type,
    expected_config_model: type,
):
    # execute
    sentence_generator_cls, sentence_generator_config_model = _select_class_and_config_model(sentence_generator_type)  # noqa

    # assert
    assert sentence_generator_cls is expected_class
    assert sentence_generator_config_model is expected_config_model


def test_select_class_and_config_model_raise_value_error():
    # execute
    with pytest.raises(ValueError):
        _select_class_and_config_model("invalid_key_monitor_type")  # type: ignore  # noqa


@pytest.mark.parametrize(
    "sentence_generator_type, sentence_generator_config, expected_class",
    [
        (
            ESentenceGeneratorType.OPENAI,
            OpenAISentenceGeneratorConfigModel(),
            OpenaiSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.STATIC,
            StaticSentenceGeneratorConfigModel(text_kana_map={}),
            StaticSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.OPENAI,
            BaseSentenceGeneratorConfigModel(),
            OpenaiSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.STATIC,
            BaseSentenceGeneratorConfigModel(),
            StaticSentenceGenerator,
        ),
    ]
    + (
        [
            (
                ESentenceGeneratorType.HUGGINGFACE,
                HuggingfaceSentenceGeneratorConfigModel(),
                HuggingfaceSentenceGenerator,
            ),
            (
                ESentenceGeneratorType.HUGGINGFACE,
                BaseSentenceGeneratorConfigModel(),
                HuggingfaceSentenceGenerator,
            ),
        ]
        if HUGGINGFACE_SETUP
        else []
    ),
)
def test_create_sentence_generator(
    sentence_generator_type: ESentenceGeneratorType,
    sentence_generator_config: BaseSentenceGeneratorConfigModel,
    expected_class: type,
    mocker,
):
    # mock
    # for OpenaiSentenceGenerator
    mocker.patch("simple_typing_application.sentence_generator.openai_sentence_generator.ChatOpenAI")  # noqa
    # for HuggingfaceSentenceGenerator
    if HUGGINGFACE_SETUP:
        mocker.patch(
            "simple_typing_application.sentence_generator.huggingface_sentence_generator.AutoModelForCausalLM.from_pretrained"
        )  # noqa
        mocker.patch(
            "simple_typing_application.sentence_generator.huggingface_sentence_generator.AutoTokenizer.from_pretrained"
        )  # noqa
        mocker.patch("simple_typing_application.sentence_generator.huggingface_sentence_generator.pipeline")  # noqa
    # for StaticSentenceGenerator
    # None

    # execute
    sentence_generator = create_sentence_generator(
        sentence_generator_type,
        sentence_generator_config,
    )

    # assert
    assert isinstance(sentence_generator, expected_class)


def test_create_sentence_generator_raise_import_error(mocker):
    # mock
    mocker.patch(
        "simple_typing_application.sentence_generator.factory._select_class_and_config_model",  # noqa
        side_effect=NameError,
    )

    # execute
    with pytest.raises(ImportError):
        create_sentence_generator(
            ESentenceGeneratorType.HUGGINGFACE,
            {},
        )


def test_create_sentence_generator_raise_value_error(mocker):
    # mock
    mocker.patch(
        "simple_typing_application.sentence_generator.factory._select_class_and_config_model",  # noqa
        side_effect=ValueError,
    )

    # execute
    with pytest.raises(ValueError):
        create_sentence_generator(
            "invalid_sentence_generator_type",  # type: ignore
            {},
        )
