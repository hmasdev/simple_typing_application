import pytest
from sdk.enum import EComponent
from sdk.create.main import main


@pytest.mark.sdk
@pytest.mark.parametrize(
    'component,input_module_name,input_class_name',
    [
        (EComponent.KEY_MONITOR, 'module0', 'class0'),
        (EComponent.SENTENCE_GENERATOR, 'module1', 'class1'),
        (EComponent.UI, 'module2', 'class2'),
    ]
)
def test_main(
    component: EComponent,
    input_module_name: str,
    input_class_name: str,
    mocker
):
    # mock
    mock_ask_module_name_for_create = mocker.patch('sdk.create.main.ask_module_name_for_create', return_value=input_module_name)  # noqa
    mock_ask_class_name_for_create = mocker.patch('sdk.create.main.ask_class_name_for_create', return_value=input_class_name)  # noqa
    mock_create_template = mocker.patch('sdk.create.main.create_template', return_value='')  # noqa
    # exec
    main(component)
    # assert
    mock_ask_module_name_for_create.assert_called_once_with(component)
    mock_ask_class_name_for_create.assert_called_once_with(component)
    mock_create_template.assert_called_once_with(component, input_module_name, input_class_name, with_file_update=True)  # noqa
