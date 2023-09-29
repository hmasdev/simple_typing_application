import inspect
import os
from ..const import (
    COMPONENT_BASE_CONFIG_MODEL_MAP,
    COMPONENT_ENUMNAME_MAP,
    COMPONENT_NAME_MAP,
    COMPONENT_SUBPACKAGE_MAP,
    COMPONENT_SUBPACKAGE_DIR_MAP,
    PACKAGE_DIR,
)
from ..enum import EComponent


def update_enum(
    component: EComponent,
    class_alias: str,
    with_file_update: bool = False,
) -> str:

    # preparation
    component_name: str = COMPONENT_NAME_MAP[component]
    const_module_path: str = os.path.join(PACKAGE_DIR, 'const', f'{component_name}.py')  # noqa
    enum_name: str = COMPONENT_ENUMNAME_MAP[component]

    # file read
    with open(const_module_path, 'r', encoding='utf-8') as f:
        contents: str = f.read()

    # update
    replace_target = f'class {enum_name}(Enum):'
    assert replace_target in contents
    contents = contents.replace(
        replace_target,
        '\n'.join([
            replace_target,
            f"    {class_alias}: str = '{class_alias}'",
        ]),
        1,
    )

    # file update
    if with_file_update:
        with open(const_module_path, 'w', encoding='utf-8') as f:
            f.write(contents)

    return contents


def create_config_model(
    component: EComponent,
    created_class: type,
    config_model_name: str,
    with_file_update: bool = False,
) -> str:

    # preparation
    component_name: str = COMPONENT_NAME_MAP[component]
    base_config_model: str = COMPONENT_BASE_CONFIG_MODEL_MAP[component]
    model_module_path: str = os.path.join(PACKAGE_DIR, 'models', 'config_models', f'{component_name}_config_model.py')  # noqa

    # extract the args and kwargs of __init__
    sig = inspect.signature(created_class)

    # file read
    with open(model_module_path, 'r', encoding='utf-8') as f:
        contents: str = f.read()

    # create contents
    attributes: list[str] = [
        ''.join([
            # e.g. '    hoge: str'
            #      '    fuga'
            #      '    piyo = 1'
            #      '    hogehoge: int = 1'
            f'    {name}',
            (f': {param.annotation.__name__}' if param.annotation != sig.empty else ''),  # noqa
            (f' = {param.default}' if param.default != sig.empty else ''),
        ])
        for name, param in sig.parameters.items()
        if name not in ('self', 'logger') and param.kind not in (param.VAR_POSITIONAL, param.VAR_KEYWORD)  # noqa
    ]

    contents = f"""{contents}\n
class {config_model_name}({base_config_model}):
""" + ('\n'.join(attributes) if attributes else '    pass') + '\n'

    # file update
    if with_file_update:
        with open(model_module_path, 'w', encoding='utf-8') as f:
            f.write(contents)

    return contents


def update_factory(
    component: EComponent,
    module_name: str,
    class_name: str,
    class_alias: str,
    config_model_name: str,
    with_file_update: bool = False,
) -> str:

    # preparation
    component_name: str = COMPONENT_NAME_MAP[component]
    enum_name: str = COMPONENT_ENUMNAME_MAP[component]
    factory_module_path: str = os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[component], 'factory.py')  # noqa

    # file read
    with open(factory_module_path, 'r', encoding='utf-8') as f:
        contents = f.read()

    # update
    replace_target = f'from ..const.{component_name} import {enum_name}'
    assert replace_target in contents
    contents = contents.replace(
        replace_target,
        '\n'.join([
            f'from .{module_name} import {class_name}',
            replace_target,
        ]),
        1,
    )
    replace_target = f'from ..models.config_models.{component_name}_config_model import (  # noqa'  # noqa
    if replace_target not in contents:
        replace_target = replace_target.replace('  # noqa', '')
    assert replace_target in contents
    contents = contents.replace(
        replace_target,
        '\n'.join([
            replace_target,
            f'    {config_model_name},',
        ]),
        1,
    )
    splitted_contents = contents.split(f'def _select_class_and_config_model', maxsplit=1)  # noqa
    splitted_contents = splitted_contents[:1] + splitted_contents[1].split('    else:', maxsplit=1)  # noqa
    contents = ''.join([
        splitted_contents[0],
        'def _select_class_and_config_model',
        splitted_contents[1],
        f'    elif {component_name}_type == {enum_name}.{class_alias}:\n',
        f'        return {class_name}, {config_model_name}\n',
        '    else:',
        splitted_contents[2],
    ])

    if with_file_update:
        with open(factory_module_path, 'w', encoding='utf-8') as f:
            f.write(contents)

    return contents


def update_subpackage_init(
    component: EComponent,
    module_name: str,
    with_file_update: bool = False,
) -> str:

    # preparation
    subpackage_dir: str = COMPONENT_SUBPACKAGE_DIR_MAP[component]

    # file read
    with open(os.path.join(subpackage_dir, '__init__.py'), 'r', encoding='utf-8') as f:  # noqa
        contents = f.read()

    # update
    contents = contents.replace(
        'from . import (\n',
        f'from . import (\n    {module_name},\n',
        1,
    )
    contents = contents.replace(
        '    base.__name__,\n',
        f'    base.__name__,\n    {module_name}.__name__,\n',
        1,
    )

    # file update
    if with_file_update:
        with open(os.path.join(subpackage_dir, '__init__.py'), 'w', encoding='utf-8') as f:  # noqa
            f.write(contents)

    return contents


def update_test_of_factory(
    component: EComponent,
    module_name: str,
    class_name: str,
    class_alias: str,
    config_model_name: str,
    with_file_update: bool = False,
) -> str:

    # preparation
    component_name: str = COMPONENT_NAME_MAP[component]
    subpackage: str = COMPONENT_SUBPACKAGE_MAP[component]
    subpackage_dir: str = COMPONENT_SUBPACKAGE_DIR_MAP[component]
    test_module_path: str = os.path.join(subpackage_dir.replace(PACKAGE_DIR, './tests'), 'test_factory.py')  # noqa
    enum_name: str = COMPONENT_ENUMNAME_MAP[component]

    # file read
    with open(test_module_path, 'r', encoding='utf-8') as f:  # noqa
        contents = f.read()

    # update
    # update import config model
    replace_target = f'simple_typing_application.models.config_models.{component_name}_config_model import (  # noqa'  # noqa
    assert replace_target in contents
    contents = contents.replace(
        replace_target,
        '\n'.join([
            replace_target,
            f'    {config_model_name},',
        ]),
        1,
    )
    # update import class
    replace_target = f'from {subpackage}.factory import ('
    assert replace_target in contents
    contents = contents.replace(
        replace_target,
        '\n'.join([
            f'from {subpackage}.{module_name} import {class_name}  # noqa',
            replace_target,
        ]),
        1,
    )
    # update test_select_class_and_config_model
    replace_target = '\n'.join([
        '    ]',
        ')',
        'def test_select_class_and_config_model(',
    ])
    if replace_target not in contents:
        replace_target = replace_target.replace(']', '],')
    assert replace_target in contents
    contents = contents.replace(
        replace_target,
        '\n'.join([
            f'        ({enum_name}.{class_alias}, {class_name}, {config_model_name}),  # noqa',  # noqa
            replace_target,
        ]),
        1,
    )
    # update test_create_...
    replace_target = '\n'.join([
        '    ]',
        ')',
        f'def test_create_{component_name}(',
    ])
    if replace_target not in contents:
        replace_target = replace_target.replace(']', '],')
    assert replace_target in contents
    contents = contents.replace(
        replace_target,
        '\n'.join([
            f'        ({enum_name}.{class_alias}, {config_model_name}().model_dump(), {class_name}),  # noqa',  # noqa
            replace_target,
        ]),
        1,
    )

    # file update
    if with_file_update:
        with open(test_module_path, 'w', encoding='utf-8') as f:
            f.write(contents)

    return contents
