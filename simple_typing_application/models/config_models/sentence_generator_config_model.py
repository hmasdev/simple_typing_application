from pydantic import BaseModel


class BaseSentenceGeneratorConfigModel(BaseModel):
    pass


class OpenAISentenceGeneratorConfigModel(BaseSentenceGeneratorConfigModel):
    model: str = 'gpt-3.5-turbo-16k'
    temperature: float = 0.7
    openai_api_key: str | None = None
    memory_size: int = 0
    max_retry: int = 5


class HuggingfaceSentenceGeneratorConfigModel(BaseSentenceGeneratorConfigModel):  # noqa
    model: str = 'line-corporation/japanese-large-lm-3.6b'
    max_length: int = 100
    do_sample: bool = True
    top_k: int = 50
    top_p: float = 0.95
    device: str = 'cuda'


class StaticSentenceGeneratorConfigModel(BaseSentenceGeneratorConfigModel):
    text_kana_map: dict[str, str | None] = {
        "これはサンプルの文章です。": "これはさんぷるのぶんしょうです。",
        "This is a sample text.": "This is a sample text.",
    }
    is_random: bool = False
