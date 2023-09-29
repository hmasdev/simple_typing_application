from importlib import import_module
from .ask import (
    ask_class_alias,
    ask_class_name,
    ask_config_model_name,
    ask_module_name,
)
from .execute import (
    create_config_model,
    update_enum,
    update_factory,
    update_subpackage_init,
    update_test_of_factory,
)
from ..const import COMPONENT_SUBPACKAGE_MAP
from ..enum import EComponent


def main(component: EComponent):

    # preparation
    subpackage: str = COMPONENT_SUBPACKAGE_MAP[component]

    # Ask
    module_name = ask_module_name(component)
    module = import_module('.'.join([subpackage, module_name.replace('.py', '')]))  # noqa
    # Ask the name of class
    class_name = ask_class_name(component, module)
    cls = getattr(module, class_name)
    # Ask the alias of the class
    class_alias = ask_class_alias(component, class_name)
    # Ask the name of config model
    config_model_name = ask_config_model_name(component, class_name)

    # Create and update required files
    # Update consts
    update_enum(component, class_alias, with_file_update=True)
    # Update models
    create_config_model(component, cls, config_model_name, with_file_update=True)  # noqa
    # Update factory
    update_factory(component, module_name, class_name, class_alias, config_model_name, with_file_update=True)  # noqa
    # update __init__.py of subpackage
    update_subpackage_init(component, module_name, with_file_update=True)  # noqa
    # Update tests
    update_test_of_factory(component, module_name, class_name, class_alias, config_model_name, with_file_update=True)  # noqa
