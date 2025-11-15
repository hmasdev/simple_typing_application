from __future__ import annotations
from pydantic import BaseModel, Field


class TypingTargetModel(BaseModel):
    text: str = Field(..., description="The raw text to be typed.", min_length=1)  # noqa
    text_hiragana_alphabet_symbol: str = Field(
        ..., description="The text to be typed in hiragana, alphabet, and symbol.", min_length=1
    )  # noqa
    typing_target: list[list[str]] = Field([], description="The typing target.")  # noqa
