import os
from .template import COMPONENT_TEMPLATE_MAP
from ..const import COMPONENT_SUBPACKAGE_DIR_MAP
from ..enum import EComponent


def create_template(
    component: EComponent,
    module_name: str,
    class_name: str,
    with_file_update: bool = False,
) -> str:
    # preparation
    module_path: str = os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[component], module_name)  # noqa
    if not module_path.endswith('.py'):
        module_path += '.py'
    # Create contents of module
    contents: str = COMPONENT_TEMPLATE_MAP[component].format(
        module_name=os.path.basename(module_path).replace('.py', ''),
        class_name=class_name,
    )
    # Create module
    if with_file_update:
        with open(module_path, 'w', encoding='utf-8') as f:
            f.write(contents)

    return contents
