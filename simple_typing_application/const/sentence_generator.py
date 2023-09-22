from enum import Enum


class ESentenceGeneratorType(Enum):
    OPENAI: str = 'OPENAI'
    HUGGINGFACE: str = 'HUGGINGFACE'
    STATIC: str = 'STATIC'
