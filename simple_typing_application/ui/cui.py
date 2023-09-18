from .base import BaseUserInterface
from ..const.color import EColor, ecolor2terminalcolor_map


class ConsoleUserInterface(BaseUserInterface):

    def show_typing_target(
        self,
        text: str,
        *,
        title: str = "",
        color: EColor = EColor.DEFAULT,
        title_color: EColor = EColor.DEFAULT,
    ) -> None:
        text = f'{ecolor2terminalcolor_map[color]}{text}{ecolor2terminalcolor_map[EColor.END]}'  # noqa
        if title:
            title = f'[{ecolor2terminalcolor_map[title_color]}{title}{ecolor2terminalcolor_map[EColor.END]}]'  # noqa
            text = f'{title} {text}'
        print(text, flush=True)

    def show_user_input(
        self,
        text: str,
        *,
        color: EColor = EColor.DEFAULT
    ) -> None:
        text = f'{ecolor2terminalcolor_map[color]}{text}{ecolor2terminalcolor_map[EColor.END]}'  # noqa
        print(text, end='', flush=True)

    def system_anounce(
        self,
        text: str,
        *,
        color: EColor = EColor.DEFAULT
    ) -> None:
        text = f'{ecolor2terminalcolor_map[color]}{text}{ecolor2terminalcolor_map[EColor.END]}'  # noqa
        print(text, flush=True)
