
from .ask import ask_class_name_for_create, ask_module_name_for_create
from .execute import create_template
from ..enum import EComponent


def main(component: EComponent):

    # Ask
    # Ask the name of module
    module_name = ask_module_name_for_create(component)
    # Ask the name of class
    class_name = ask_class_name_for_create(component)

    # Create module
    create_template(component, module_name, class_name, with_file_update=True)  # noqa
