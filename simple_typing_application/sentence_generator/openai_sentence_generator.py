from __future__ import annotations
from datetime import datetime as dt
from logging import DEBUG, Logger, getLogger
from typing import Any, Callable, cast

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, SecretStr

from .base import BaseSentenceGenerator
from ..models.typing_target_model import TypingTargetModel
from .utils import split_hiraganas_alphabets_symbols, splitted_hiraganas_alphabets_symbols_to_typing_target  # noqa
from ..utils.japanese_string_utils import delete_space_between_hiraganas
from ..utils.rerun import rerun_deco
from ..utils.stopwatch import stopwatch


class _OutputSchema(BaseModel):
    text: str = Field(..., description="生成された一文")
    text_hiragana_alphabet_symbol: str = Field(  # noqa
        ...,
        description="一文をひらがな、アルファベット、記号のみに変換したもの",  # noqa
    )

    def build_typing_target(self) -> TypingTargetModel:
        dic: dict[str, str | list[list[str]]] = {}
        # assign values
        dic["text"] = self.text
        # delete space between hiraganas
        dic["text_hiragana_alphabet_symbol"] = delete_space_between_hiraganas(self.text_hiragana_alphabet_symbol)
        # create typing target
        splitted = split_hiraganas_alphabets_symbols(self.text_hiragana_alphabet_symbol)
        dic["typing_target"] = splitted_hiraganas_alphabets_symbols_to_typing_target(splitted)  # noqa
        return TypingTargetModel(**dic)


class OpenaiSentenceGenerator(BaseSentenceGenerator):
    def __init__(
        self,
        model: str = "gpt-5-nano",
        temperature: float = 0.7,
        openai_api_key: SecretStr | str | None = None,
        memory_size: int = 5,
        max_retry: int = 5,
        seed: int | None = None,
        logger: Logger = getLogger(__name__),
    ):
        chat_model = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_retries=max_retry,
            api_key=((lambda: openai_api_key) if isinstance(openai_api_key, str) else openai_api_key),
            reasoning_effort="minimal" if model.startswith("gpt-5") else None,
            seed=seed,
        )
        self._agent = create_agent(
            model=chat_model,
            response_format=_OutputSchema,
        )
        self._memory: list[_OutputSchema] = []
        self._memory_size = memory_size
        self.generate = rerun_deco(  # type: ignore
            self.generate,
            max_retry=max_retry,
            callback=self._retry_callback,
            logger=logger,
        )
        self._logger = logger

    def _retry_callback(self) -> None:
        if self._memory:
            self._logger.info(f"reducing memory size: {len(self._memory)} -> {len(self._memory) - 1}")
            del self._memory[0]

    async def generate(
        self,
        callback: Callable[[TypingTargetModel], TypingTargetModel] | None = None,  # noqa
    ) -> TypingTargetModel:
        # invoke agent
        messages = [
            {
                "role": "system",
                "content": self._system_prompt,
            },
            {
                "role": "user",
                "content": self._user_prompt,
            },
        ]
        self._logger.debug(f"agent input messages: {messages}")
        with stopwatch(level=DEBUG, logger=self._logger, prefix="OpenAI agent invocation"):
            ret: dict[str, Any] = await self._agent.ainvoke(
                {"messages": messages},  # type: ignore
            )
        self._logger.debug(f"agent response: {ret}")

        # store to memory
        output = cast(_OutputSchema, ret["structured_response"])
        self._memory.append(output)
        if len(self._memory) > self._memory_size:
            self._memory.pop(0)

        # build typing target
        cleaned_ret: TypingTargetModel = output.build_typing_target()

        if callback is None:
            return cleaned_ret
        else:
            return callback(cleaned_ret)

    @property
    def _system_prompt(self) -> str:
        key = dt.now().strftime("%Y/%m/%d %H:%M:%S.%f")[::-1]
        past_outputs = "\n".join(["- `" + m.model_dump_json(indent=None) + "`" for m in self._memory])
        return f"""あなたは非常に優秀な日本語の短文作家です。
あなたが素晴らしいと思う 20 文字以上の日本語の一文を下記の手順で step-by-step に生成してください。

Step 1. 20文字以上の日本語の一文を生成する。
Step 2. Step 1 で生成した一文に含まれる漢字もしくはカタカナをひらがなに変換する。

出力は下記の JSON のフォーマットとします。

```json
{{
    "text": "Step 1 で生成した一文",
    "text_hiragana_alphabet_symbol": "Step 2 で変換した文章",
}}
```

なお、下記の事項も遵守してください。
- json のフォーマットは厳守してください。
- json 以外の出力は一切行わないでください。
- text_hiragana_alphabet_symbol は、ひらがなもしくはアルファベット、記号のみを含むこと。カタカナおよび漢字は絶対に含めないでください。
- 不要な空白文字は含まないこと。例えば、text が '今日も元気に' の場合は text_hiragana_alphabet_symbol は 'きょう も げんき に' のように単語間に空白を挿入するのではなく 'きょうもげんきに' としてください。
- 過去に出力した結果と類似する結果は出力しないでください。
- 出力は結果のみとしてください。

過去の出力
{past_outputs}

乱数シード：{key}
"""  # noqa

    @property
    def _user_prompt(self) -> str:
        return "生成してください。"
