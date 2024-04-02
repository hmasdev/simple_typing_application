from __future__ import annotations
from datetime import datetime as dt
import json
from logging import getLogger, Logger
from typing import Callable

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.pydantic_v1 import SecretStr

from .base import BaseSentenceGenerator
from ..models.typing_target_model import TypingTargetModel
from .utils import split_hiraganas_alphabets_symbols, splitted_hiraganas_alphabets_symbols_to_typing_target  # noqa
from ..utils.japanese_string_utils import delete_space_between_hiraganas
from ..utils.rerun import rerun_deco


class OpenaiSentenceGenerator(BaseSentenceGenerator):

    def __init__(
        self,
        model: str = 'gpt-3.5-turbo-16k',
        temperature: float = .7,
        openai_api_key: SecretStr | None = None,
        memory_size: int = 1,
        max_retry: int = 5,
        logger: Logger = getLogger(__name__),
    ):
        self._max_retry = max_retry

        self._llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=openai_api_key,
        )
        self._memory = ConversationBufferMemory(k=memory_size)  # type: ignore  # noqa
        self._chain = ConversationChain(llm=self._llm, memory=self._memory)  # type: ignore  # noqa
        self.generate = rerun_deco(self.generate, max_retry=max_retry, callback=self._memory.clear, logger=logger)  # type: ignore  # noqa
        self._logger = logger

    async def generate(
        self,
        callback: Callable[[TypingTargetModel], TypingTargetModel] | None = None,  # noqa
    ) -> TypingTargetModel:
        ret: str = await self._chain.arun(self._prompt)  # type: ignore
        self._logger.debug(f'chain response: {ret}')
        if callback is None:
            return self.clean(ret)
        else:
            return callback(self.clean(ret))

    @property
    def _prompt(self) -> str:
        key = dt.now().strftime("%Y/%m/%d %H:%M:%S.%f")[::-1]
        return f'''あなたは非常に優秀な日本語の短文作家です。
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

乱数シード：{key}
'''  # noqa

    def clean(self, s: str) -> TypingTargetModel:
        # extract the json part
        s = s.split("{")[-1].split("}")[0]
        s = "{" + s + "}"
        # convert to dict
        dic = json.loads(s)
        # delete space between hiraganas
        dic['text_hiragana_alphabet_symbol'] = delete_space_between_hiraganas(dic['text_hiragana_alphabet_symbol'])  # noqa
        # create typing target
        splitted = split_hiraganas_alphabets_symbols(dic['text_hiragana_alphabet_symbol'])  # noqa
        self._logger.debug(f'splitted pattern: {splitted}')
        dic['typing_target'] = splitted_hiraganas_alphabets_symbols_to_typing_target(splitted)  # noqa
        self._logger.debug(f'typing target: {dic["typing_target"]}')
        # convert to TypingTargetModel
        return TypingTargetModel(**dic)
