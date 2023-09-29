import os
import pytest
from sdk.const import COMPONENT_SUBPACKAGE_DIR_MAP
from sdk.create.execute import create_template
from sdk.create.template import COMPONENT_TEMPLATE_MAP
from sdk.enum import EComponent


def generate_valid_module_name(
    module_name: str,
    direc: str,
    ext: str = '.py',
) -> str:

    # create
    path = os.path.join(direc, module_name)
    if not path.endswith(ext):
        path += ext

    # return
    if os.path.exists(path):
        # NOTE: if file exists, add '_' to filename and call recursively
        return generate_valid_module_name(module_name + '_', direc, ext)
    else:
        return module_name


@pytest.mark.sdk
@pytest.mark.parametrize(
    'component, module_name, class_name, with_file_update, expected_template',
    [
        (
            EComponent.KEY_MONITOR,
            generate_valid_module_name('hoge', direc=COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.KEY_MONITOR], ext='.py'),  # noqa
            'Hoge',
            False,
            COMPONENT_TEMPLATE_MAP[EComponent.KEY_MONITOR],
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            generate_valid_module_name('hoge', direc=COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], ext='.py'),  # noqa
            'Hoge',
            False,
            COMPONENT_TEMPLATE_MAP[EComponent.SENTENCE_GENERATOR],
        ),
        (
            EComponent.UI,
            generate_valid_module_name('hoge', direc=COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.UI], ext='.py'),  # noqa
            'Hoge',
            False,
            COMPONENT_TEMPLATE_MAP[EComponent.UI],
        ),
        (
            EComponent.KEY_MONITOR,
            generate_valid_module_name('hoge', direc=COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.KEY_MONITOR], ext='.py'),  # noqa
            'Hoge',
            True,
            COMPONENT_TEMPLATE_MAP[EComponent.KEY_MONITOR],
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            generate_valid_module_name('hoge', direc=COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.SENTENCE_GENERATOR], ext='.py'),  # noqa
            'Hoge',
            True,
            COMPONENT_TEMPLATE_MAP[EComponent.SENTENCE_GENERATOR],
        ),
        (
            EComponent.UI,
            generate_valid_module_name('hoge', direc=COMPONENT_SUBPACKAGE_DIR_MAP[EComponent.UI], ext='.py'),  # noqa
            'Hoge',
            True,
            COMPONENT_TEMPLATE_MAP[EComponent.UI],
        ),
    ]
)
def test_create_template(
    component: EComponent,
    module_name: str,
    class_name: str,
    with_file_update: bool,
    expected_template: str,
    mocker,
):
    # mock
    mock_open = mocker.patch('builtins.open', new_callable=mocker.mock_open)

    # preparation
    expected = expected_template.format(class_name=class_name, module_name=module_name)  # noqa

    # exec
    actual = create_template(component, module_name, class_name, with_file_update)  # noqa

    # assert
    assert actual == expected
    if with_file_update:
        mock_open.assert_called_once_with(
            os.path.join(COMPONENT_SUBPACKAGE_DIR_MAP[component], f"{module_name}.py"),  # noqa
            'w',
            encoding='utf-8'
        )
        mock_open().write.assert_called_once_with(expected)
