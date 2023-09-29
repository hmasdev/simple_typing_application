from logging import Logger, getLogger

import click

from .create.main import main as create_main
from .enum import EComponent, ETask
from .integrate.main import main as integrate_main
from .util import input_until_valid


def ask_for_task(default: ETask = ETask.CREATE) -> ETask:
    return input_until_valid(  # type: ignore
        '\n'.join([
            'What do you want to do?'
        ] + [
            f'{task.value}: {task.name}'
            for task in ETask
        ] + [
            f'Enter the number of the task you want to do (Defaults: {default.value}): ',  # noqa
        ]),
        is_valid=dict(
            **{str(task.value): task for task in ETask},
            **{"": default}
        ).__contains__,
        callback=dict(
            **{str(task.value): task for task in ETask},
            **{"": default}
        ).get,
    )


def ask_for_component(
    task: ETask,
    default: EComponent = EComponent.SENTENCE_GENERATOR,
) -> EComponent:
    return input_until_valid(  # type: ignore
        '\n'.join([
            f'Which kind of task do you want to {task.name.lower()}?',
        ] + [
            f'{kind.value}: {kind.name}'
            for kind in EComponent
        ] + [
            f'Enter the number of the kind you want to {task.name.lower()} (Defaults: {default.value}): ',  # noqa
        ]),
        is_valid=dict(
            **{str(kind.value): kind for kind in EComponent},
            **{"": default},
        ).__contains__,
        callback=dict(
            **{str(kind.value): kind for kind in EComponent},
            **{"": default},
        ).get,
    )


def _cli_inner(logger: Logger = getLogger(__name__)):
    # Ask what kind of task to do
    task: ETask = ask_for_task()
    component: EComponent = ask_for_component(task)
    # Do the task
    if task == ETask.CREATE:
        create_main(component)
    elif task == ETask.INTEGRATE:
        integrate_main(component)
    else:
        raise NotImplementedError(f"Task '{task}' is not implemented.")


@click.command()
def cli() -> None:
    _cli_inner()


if __name__ == '__main__':
    cli()
