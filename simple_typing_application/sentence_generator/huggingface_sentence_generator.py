from logging import getLogger, Logger
from typing import Callable

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from .base import BaseSentenceGenerator
from ..models.typing_target_model import TypingTargetModel
from .utils import (
    split_hiraganas_alphabets_symbols,
    splitted_hiraganas_alphabets_symbols_to_typing_target,
)
from ..utils.japanese_string_utils import (
    delete_space_between_hiraganas,
    excelapi_kanji2kana,
)


class HuggingfaceSentenceGenerator(BaseSentenceGenerator):

    def __init__(
        self,
        model: str = 'line-corporation/japanese-large-lm-3.6b',
        max_length: int = 20,
        do_sample: bool = True,
        top_k: int = 50,
        top_p: float = 0.95,
        device: str = 'cuda',
        logger: Logger = getLogger(__name__),
    ) -> None:
        self._tokenizer = AutoTokenizer.from_pretrained(model, use_fast=False)  # noqa
        self._model = AutoModelForCausalLM.from_pretrained(model, torch_dtype=torch.float16)  # noqa
        self._generator = pipeline('text-generation', model=self._model, tokenizer=self._tokenizer, device=device)  # noqa
        self._max_length = max_length
        self._do_sample = do_sample
        self._top_k = top_k
        self._top_p = top_p
        self._logger = logger

    async def generate(
        self,
        callback: Callable[[TypingTargetModel], TypingTargetModel] | None = None,  # noqa
    ) -> TypingTargetModel:

        # generate
        ret = self._generator(
            self._prompt,
            max_length=self._max_length,
            do_sample=self._do_sample,
            top_k=self._top_k,
            top_p=self._top_p,
            pad_token_id=self._tokenizer.pad_token_id
        )

        # postprocess
        generated_text: str = delete_space_between_hiraganas(ret[0]['generated_text'])  # noqa
        generated_text = generated_text.replace(self._prompt, '')
        generated_text = generated_text.split('。')[0] + ('。' if '。' in generated_text else '')  # noqa
        self._logger.debug(f'generated text: {generated_text}')
        hiragana_text: str = excelapi_kanji2kana(generated_text)
        self._logger.debug(f'generated text (hira): {hiragana_text}')
        splitted: list[str] = split_hiraganas_alphabets_symbols(hiragana_text)  # noqa
        self._logger.debug(f'splitted pattern: {splitted}')
        typing_target: list[list[str]] = splitted_hiraganas_alphabets_symbols_to_typing_target(splitted)  # noqa
        self._logger.debug(f'typing target: {typing_target}')

        if callback is None:
            return TypingTargetModel(
                text=generated_text,
                text_hiragana_alphabet_symbol=hiragana_text,
                typing_target=typing_target,
            )
        else:
            return callback(TypingTargetModel(
                text=generated_text,
                text_hiragana_alphabet_symbol=hiragana_text,
                typing_target=typing_target,
            ))

    @property
    def _prompt(self) -> str:
        return '日本語の例文: ・'
