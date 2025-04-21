from enum import Enum


class ESentenceGeneratorType(Enum):
    OPENAI = 'OPENAI'
    HUGGINGFACE = 'HUGGINGFACE'
    STATIC = 'STATIC'
