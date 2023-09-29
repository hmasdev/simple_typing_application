import pytest
from sdk.enum import EComponent, ETask
from sdk.main import (
    ask_for_component,
    ask_for_task,
    _cli_inner,
)


@pytest.mark.sdk
@pytest.mark.parametrize(
    'task, default_component, input_returns, expected',
    [
        # fo ETask.CREATE
        (
            ETask.CREATE,
            None,
            [str(EComponent.KEY_MONITOR.value)],
            EComponent.KEY_MONITOR,
        ),
        (
            ETask.CREATE,
            None,
            [str(EComponent.SENTENCE_GENERATOR.value)],
            EComponent.SENTENCE_GENERATOR,
        ),
        (
            ETask.CREATE,
            None,
            [str(EComponent.UI.value)],
            EComponent.UI,
        ),
        (
            ETask.CREATE,
            None,
            ['_invalid', str(EComponent.UI.value)],
            EComponent.UI,
        ),
        (
            ETask.CREATE,
            None,
            [''],
            EComponent.SENTENCE_GENERATOR,
        ),
        (
            ETask.CREATE,
            EComponent.KEY_MONITOR,
            [''],
            EComponent.KEY_MONITOR,
        ),
        # for ETask.INTEGRATE
        (
            ETask.INTEGRATE,
            None,
            [str(EComponent.KEY_MONITOR.value)],
            EComponent.KEY_MONITOR,
        ),
        (
            ETask.INTEGRATE,
            None,
            [str(EComponent.SENTENCE_GENERATOR.value)],
            EComponent.SENTENCE_GENERATOR,
        ),
        (
            ETask.INTEGRATE,
            None,
            [str(EComponent.UI.value)],
            EComponent.UI,
        ),
        (
            ETask.INTEGRATE,
            None,
            ['_invalid', str(EComponent.UI.value)],
            EComponent.UI,
        ),
        (
            ETask.INTEGRATE,
            None,
            [''],
            EComponent.SENTENCE_GENERATOR,
        ),
        (
            ETask.INTEGRATE,
            EComponent.KEY_MONITOR,
            [''],
            EComponent.KEY_MONITOR,
        ),
    ]
)
def test_ask_for_component(
    task: ETask,
    default_component: EComponent | None,
    input_returns: list[str],
    expected: str,
    mocker,
):
    # mock
    mock_input = mocker.patch('builtins.input', side_effect=input_returns)
    # run
    kwargs = {} if default_component is None else {'default': default_component}  # noqa
    actual = ask_for_component(task, **kwargs)
    # assert
    assert actual == expected
    mock_input.call_count == len(input_returns)


@pytest.mark.sdk
@pytest.mark.parametrize(
    'default_task, input_returns, expected',
    [
        (
            None,
            [str(ETask.CREATE.value)],
            ETask.CREATE,
        ),
        (
            None,
            [str(ETask.INTEGRATE.value)],
            ETask.INTEGRATE,
        ),
        (
            None,
            ['_invalid', str(ETask.INTEGRATE.value)],
            ETask.INTEGRATE,
        ),
        (
            None,
            [''],
            ETask.CREATE,
        ),
        (
            ETask.INTEGRATE,
            [''],
            ETask.INTEGRATE,
        ),
    ]
)
def test_ask_for_task(
    default_task: ETask,
    input_returns: list[str],
    expected: ETask,
    mocker
):
    # mock
    mock_input = mocker.patch('builtins.input', side_effect=input_returns)
    # run
    kwargs = {} if default_task is None else {'default': default_task}
    actual = ask_for_task(**kwargs)
    # assert
    assert actual == expected
    mock_input.call_count == len(input_returns)


@pytest.mark.sdk
@pytest.mark.parametrize(
    'task, component',
    [
        (ETask.CREATE, EComponent.SENTENCE_GENERATOR),
        (ETask.CREATE, EComponent.KEY_MONITOR),
        (ETask.CREATE, EComponent.UI),
        (ETask.INTEGRATE, EComponent.SENTENCE_GENERATOR),
        (ETask.INTEGRATE, EComponent.KEY_MONITOR),
        (ETask.INTEGRATE, EComponent.UI),
    ]
)
def test__cli_inner(
    task: ETask,
    component: EComponent,
    mocker,
):
    # mock
    mock_ask_for_task = mocker.patch('sdk.main.ask_for_task', return_value=task)  # noqa
    mock_ask_for_component = mocker.patch('sdk.main.ask_for_component', return_value=component)  # noqa
    mock_create_main = mocker.patch('sdk.main.create_main')
    mock_integrate_main = mocker.patch('sdk.main.integrate_main')
    # run
    _cli_inner()
    # assert
    mock_ask_for_task.assert_called_once()
    mock_ask_for_component.assert_called_once()
    if task == ETask.CREATE:
        mock_create_main.assert_called_once_with(component)
        mock_integrate_main.assert_not_called()
    elif task == ETask.INTEGRATE:
        mock_create_main.assert_not_called()
        mock_integrate_main.assert_called_once_with(component)
