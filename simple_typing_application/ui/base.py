from abc import ABC, abstractmethod
from ..const.color import EColor


class BaseUserInterface(ABC):

    @abstractmethod
    def show_typing_target(
        self,
        text: str,
        *,
        title: str = "",
        color: EColor = EColor.DEFAULT,
        title_color: EColor = EColor.DEFAULT,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def show_user_input(
        self,
        text: str,
        *,
        color: EColor = EColor.DEFAULT,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def system_anounce(
        self,
        text: str,
        *,
        color: EColor = EColor.DEFAULT,
    ) -> None:
        raise NotImplementedError()
