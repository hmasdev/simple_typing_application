from __future__ import annotations
from logging import getLogger, Logger
import time
from typing import Callable
import random

from .base import BaseSentenceGenerator
from ..models.typing_target_model import TypingTargetModel
from .utils import (
    split_hiraganas_alphabets_symbols,
    splitted_hiraganas_alphabets_symbols_to_typing_target,
)
from ..utils.japanese_string_utils import excelapi_kanji2kana


class StaticSentenceGenerator(BaseSentenceGenerator):
    __WAIT_TIME_SEC: float = 1.0

    def __init__(
        self,
        text_kana_map: dict[str, str | None],
        is_random: bool = False,
        logger: Logger = getLogger(__name__),
    ) -> None:
        self._text_kana_pairs = tuple(
            (k, v if v is not None else self._kanji2kana(k)) for k, v in text_kana_map.items()
        )
        self._is_random: bool = is_random
        self._index: int = -1
        self._logger = logger

    async def generate(
        self,
        callback: Callable[[TypingTargetModel], TypingTargetModel] | None = None,  # noqa
    ) -> TypingTargetModel:
        # generate
        generated_text, generated_kana = self._get_next()
        self._logger.debug(f"generated text: {generated_text}")
        self._logger.debug(f"generated kana: {generated_kana}")

        # postprocess
        splitted = split_hiraganas_alphabets_symbols(generated_kana)
        self._logger.debug(f"splitted pattern: {splitted}")
        typing_target = splitted_hiraganas_alphabets_symbols_to_typing_target(splitted)  # noqa
        self._logger.debug(f"typing target: {typing_target}")

        # callback
        if callback is None:
            return TypingTargetModel(
                text=generated_text,
                text_hiragana_alphabet_symbol=generated_kana,
                typing_target=typing_target,
            )
        else:
            return callback(
                TypingTargetModel(
                    text=generated_text,
                    text_hiragana_alphabet_symbol=generated_kana,
                    typing_target=typing_target,
                )
            )

    def _get_next(self) -> tuple[str, str]:
        # get index
        if self._is_random:
            self._index = random.randint(0, len(self._text_kana_pairs) - 1)
        else:
            self._index = (self._index + 1) % len(self._text_kana_pairs)

        return self._text_kana_pairs[self._index]

    def _kanji2kana(self, text: str) -> str:
        time.sleep(self.__WAIT_TIME_SEC)
        return excelapi_kanji2kana(text)
