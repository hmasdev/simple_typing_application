import os
from ..const import COMPONENT_SUBPACKAGE_DIR_MAP
from ..enum import EComponent
from ..util import input_until_valid, integrate_validators


def ask_module_name_for_create(component: EComponent) -> str:
    return input_until_valid(
        'Enter the name of the module which you want to create (e.g. hoge): ',
        is_valid=integrate_validators(
            (
                lambda x: len(x) > 0,
                lambda x: x[0].isalpha() or x[0] == '_',
                lambda x: all(map(lambda c: c.isalnum() or c == '_', x)),
                lambda x: (not os.path.exists(os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[component], f'{x}.py'))),  # noqa
            ),
            (
                'Module name must not be empty.',
                'Module name must start with alphabet or underscore.',
                'Module name must be composed of alphabets, numbers, and underscores.',  # noqa
                'Module name must not be duplicated.',
            ),
        ),
    )


def ask_class_name_for_create(component: EComponent) -> str:
    return input_until_valid(
        'Enter the name of the class: ',
        is_valid=integrate_validators(
            (
                lambda x: len(x) > 0,
                lambda x: x[0].isalpha() or x[0] == '_',
                lambda x: not x.startswith('__'),
                lambda x: all(map(lambda c: c.isalnum() or c == '_', x)),
            ),
            (
                'Class name must not be empty.',
                'Class name must start with alphabet or underscore.',
                'Class name must not start with "__".',
                'Class name must be composed of alphabets, numbers, and underscores.',  # noqa
            ),
        ),
    )
