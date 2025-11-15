from simple_typing_application.const.color import EColor, ecolor2terminalcolor_map  # noqa
from simple_typing_application.ui.cui import ConsoleUserInterface


def test_show_typing_target(mocker):
    # mock
    mock_print = mocker.patch("builtins.print")

    # preparation
    cui = ConsoleUserInterface()
    text = "Hello, World!"
    title = "title"
    color = EColor.RED
    title_color = EColor.BLUE
    expected = f"[{ecolor2terminalcolor_map[EColor.BLUE]}{title}{ecolor2terminalcolor_map[EColor.END]}] {ecolor2terminalcolor_map[EColor.RED]}{text}{ecolor2terminalcolor_map[EColor.END]}"  # noqa

    # execute
    cui.show_typing_target(text, title=title, color=color, title_color=title_color)  # noqa

    # asert
    mock_print.assert_called_once_with(expected, flush=True)


def test_show_user_input(mocker):
    # mock
    mock_print = mocker.patch("builtins.print")

    # preparation
    cui = ConsoleUserInterface()
    text = "Hello, World!"
    color = EColor.RED
    expected = f"{ecolor2terminalcolor_map[EColor.RED]}{text}{ecolor2terminalcolor_map[EColor.END]}"  # noqa

    # execute
    cui.show_user_input(text, color=color)

    # asert
    mock_print.assert_called_once_with(expected, end="", flush=True)


def test_system_anounce(mocker):
    # mock
    mock_print = mocker.patch("builtins.print")

    # preparation
    cui = ConsoleUserInterface()
    text = "Hello, World!"
    color = EColor.RED
    expected = f"{ecolor2terminalcolor_map[EColor.RED]}{text}{ecolor2terminalcolor_map[EColor.END]}"  # noqa

    # execute
    cui.system_anounce(text, color=color)

    # asert
    mock_print.assert_called_once_with(expected, flush=True)
