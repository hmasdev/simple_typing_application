from importlib import import_module
import os
from types import ModuleType
from ..const import (
    PACKAGE_DIR,
    COMPONENT_NAME_MAP,
    COMPONENT_SUBPACKAGE_MAP,
    COMPONENT_SUBPACKAGE_DIR_MAP,
)
from ..enum import EComponent
from ..util import (
    input_until_valid,
    integrate_validators,
    error_detection_validator_deco,
)


def ask_module_name(component: EComponent) -> str:

    # Get the subpackage directory
    subpackage: str = COMPONENT_SUBPACKAGE_MAP[component]
    subpackage_dir: str = COMPONENT_SUBPACKAGE_DIR_MAP[component]

    return input_until_valid(
        'Enter the name of the module which you have created: ',
        is_valid=integrate_validators(
            (
                lambda x: os.path.exists(os.path.join(subpackage_dir, x if x.endswith('.py') else f'{x}.py')),  # noqa
                lambda x: os.path.isfile(os.path.join(subpackage_dir, x if x.endswith('.py') else f'{x}.py')),  # noqa
                lambda x: error_detection_validator_deco(import_module)('.'.join([subpackage, x.replace('.py', '')])),  # noqa
            ),
            (
                'Module not found. Check the name of the module or create the module.',  # noqa
                "Given module name is not a file but a package.",
                'Failed to import the given module. Check and fix the module',
            )
        ),
    )


def ask_class_name(component: EComponent, module: ModuleType) -> str:
    return input_until_valid(
        'Enter the name of the class which you have implemented: ',
        is_valid=integrate_validators(
            (
                lambda x: hasattr(module, x),
                lambda x: isinstance(getattr(module, x), type)
            ),
            'Class not found. Check the name of the class or create the class.',  # noqa
        ),
    )


def ask_class_alias(component: EComponent, class_name: str) -> str:

    # preparation
    component_name: str = COMPONENT_NAME_MAP[component]
    const_module_path: str = os.path.join(PACKAGE_DIR, 'const', f'{component_name}.py')  # noqa
    default_alias: str = class_name.upper()

    # validation
    assert len(default_alias) > 0
    assert default_alias[0].isalpha() or default_alias[0] == '_'
    assert default_alias not in open(const_module_path, encoding='utf-8').read()  # noqa
    assert all(map(lambda c: c.isalnum() or c == '_', default_alias))  # noqa

    return input_until_valid(
        f'Enter the alias of {class_name} (Defaults: {default_alias}): ',
        is_valid=integrate_validators(
            (
                lambda x: len(x) == 0 or (x[0].isalpha() or x[0] == '_'),
                lambda x: len(x) == 0 or (x[0].isalpha() or x[0] == '__'),
                lambda x: len(x) == 0 or (len(x) > 0 and x not in open(const_module_path, encoding='utf-8').read()),  # noqa
                lambda x: len(x) == 0 or all(map(lambda c: c.isalnum() or c == '_', x)),  # noqa
            ),
            (
                'Alias must start with alphabet or underscore.',
                'Alias must not start with "__".',
                'Alias has already been used. Try another one.',
                'Alias must be composed of alphabets, numbers, and underscores.',  # noqa
            ),
        ),
        callback=lambda x: default_alias if x == '' else x,
    )


def ask_config_model_name(component: EComponent, class_name: str) -> str:

    # preparation
    component_name: str = COMPONENT_NAME_MAP[component]
    model_module_path: str = os.path.join(PACKAGE_DIR, 'models', 'config_models', f'{component_name}_config_model.py')  # noqa
    default_config_model_name: str = f'{class_name}ConfigModel'

    # validation
    assert len(default_config_model_name) > 0
    assert default_config_model_name[0].isalpha() or default_config_model_name[0] == '_'  # noqa
    assert default_config_model_name not in open(model_module_path, encoding='utf-8').read()  # noqa
    assert all(map(lambda c: c.isalnum() or c == '_', default_config_model_name))  # noqa

    return input_until_valid(
        f'Enter the name of the config model for {class_name} (Defaults: {default_config_model_name}): ',  # noqa
        is_valid=integrate_validators(
            (
                lambda x: len(x) == 0 or (x[0].isalpha() or x[0] == '_'),
                lambda x: len(x) == 0 or (x[0].isalpha() or x[0] == '__'),
                lambda x: len(x) == 0 or (len(x) > 0 and x not in open(model_module_path, encoding='utf-8').read()),  # noqa
                lambda x: len(x) == 0 or all(map(lambda c: c.isalnum() or c == '_', x)),  # noqa
            ),
            (
                'Config model name must start with alphabet or underscore.',
                'Config model name must not start with "__".',
                'Config model name has already been used. Try another one.',
                'Config model name must be composed of alphabets, numbers, and underscores.',  # noqa
            )
        ),
        callback=lambda x: default_config_model_name if x == '' else x,
    )
