from ..enum import EComponent


_KEY_MONITOR_TEMPLATE: str = """# Path: {module_name}.py

from logging import getLogger, Logger
from typing import Callable
from .base import BaseKeyMonitor
from ..const.keys import EMetaKey


class {class_name}(BaseKeyMonitor):

    def __init__(
        self,
        logger: Logger = getLogger(__name__),
    ):
        self._on_press_callback: Callable[[EMetaKey | str | None], bool | None] | None = None  # noqa
        self._on_release_callback: Callable[[EMetaKey | str | None], bool | None] | None = None  # noqa
        self._logger = logger

    def start(self):
        # TODO: Implement this method
        pass

    def stop(self):
        # TODO: Implement this method
        pass

"""

_SENTENCE_GENERATOR_TEMPLATE = """# Path: {module_name}.py

from logging import getLogger, Logger
from .base import BaseSentenceGenerator
from ..models.typing_target_model import TypingTargetModel


class {class_name}(BaseSentenceGenerator):

    def __init__(
        self,
        logger: Logger = getLogger(__name__),
    ):
        self._logger = logger

    async def generate(
        self,
        callback: Callable[[TypingTargetModel], TypingTargetModel] = lambda x: x,  # noqa
    ) -> TypingTargetModel:
        # TODO: Implement this method
        pass

"""

_UI_TEMPLATE: str = """# Path: {module_name}.py

from logging import getLogger, Logger
from .base import BaseUserInterface
from ..const.color import EColor


class {class_name}(BaseUserInterface):

    def __init__(
        self,
        logger: Logger = getLogger(__name__),
    ):
        self._logger = logger

    def show_typing_target(
        self,
        text: str,
        *,
        title: str = "",
        color: EColor = EColor.DEFAULT,
        title_color: EColor = EColor.DEFAULT,
    ):
        # TODO: Implement this method
        pass

    def show_user_input(
        self,
        text: str,
        *,
        color: EColor = EColor.DEFAULT,
    ) -> None:
        # TODO: Implement this method
        pass

    @abstractmethod
    def system_anounce(
        self,
        text: str,
        *,
        color: EColor = EColor.DEFAULT,
    ) -> None:
        # TODO: Implement this method
        pass

"""


COMPONENT_TEMPLATE_MAP = {
    EComponent.KEY_MONITOR: _KEY_MONITOR_TEMPLATE,
    EComponent.SENTENCE_GENERATOR: _SENTENCE_GENERATOR_TEMPLATE,
    EComponent.UI: _UI_TEMPLATE,
}
