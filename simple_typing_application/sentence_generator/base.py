from abc import ABC, abstractmethod
from typing import Callable
from ..models.typing_target_model import TypingTargetModel


class BaseSentenceGenerator(ABC):
    @abstractmethod
    async def generate(
        self,
        callback: Callable[[TypingTargetModel], TypingTargetModel] = lambda x: x,  # noqa
    ) -> TypingTargetModel:
        raise NotImplementedError()
