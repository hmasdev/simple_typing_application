from types import ModuleType
import pytest
from sdk.const import COMPONENT_SUBPACKAGE_MAP
from sdk.enum import EComponent
from sdk.integrate.main import main


@pytest.mark.sdk
@pytest.mark.parametrize(
    'component,input_module_name,input_class_name,input_class_alias,input_config_model_name',  # noqa
    [
        (EComponent.KEY_MONITOR, 'module0.py', 'class0', 'Class0', 'ConfigModel0'),  # noqa
        (EComponent.SENTENCE_GENERATOR, 'module1.py', 'class1', 'Class1', 'ConfigModel1'),  # noqa
        (EComponent.UI, 'module2.py', 'class2', 'Class2', 'ConfigModel2'),
    ]
)
def test_main(
    component: EComponent,
    input_module_name: str,
    input_class_name: str,
    input_class_alias: str,
    input_config_model_name: str,
    mocker,
):
    # mock
    mock_ask_module_name = mocker.patch('sdk.integrate.main.ask_module_name', return_value=input_module_name)  # noqa
    mock_ask_class_name = mocker.patch('sdk.integrate.main.ask_class_name', return_value=input_class_name)  # noqa
    mock_ask_class_alias = mocker.patch('sdk.integrate.main.ask_class_alias', return_value=input_class_alias)  # noqa
    mock_ask_config_model_name = mocker.patch('sdk.integrate.main.ask_config_model_name', return_value=input_config_model_name)  # noqa
    mock_update_enum = mocker.patch('sdk.integrate.main.update_enum')  # noqa
    mock_create_config_model = mocker.patch('sdk.integrate.main.create_config_model')  # noqa
    mock_update_factory = mocker.patch('sdk.integrate.main.update_factory')  # noqa
    mock_update_subpackage_init = mocker.patch('sdk.integrate.main.update_subpackage_init')  # noqa
    mock_update_test_of_factory = mocker.patch('sdk.integrate.main.update_test_of_factory')  # noqa

    mock_module = mocker.MagicMock(spec=ModuleType)
    mock_class = mocker.MagicMock(spec=type)
    setattr(mock_module, input_class_name, mock_class)
    mock_import_module = mocker.patch('sdk.integrate.main.import_module', return_value=mock_module)  # noqa

    # exec
    main(component)

    # assert
    mock_ask_module_name.assert_called_once_with(component)
    mock_import_module.assert_called_once_with(f'{COMPONENT_SUBPACKAGE_MAP[component]}.{input_module_name.replace(".py", "")}')  # noqa
    mock_ask_class_name.assert_called_once_with(component, mock_module)
    mock_ask_class_alias.assert_called_once_with(component, input_class_name)
    mock_ask_config_model_name.assert_called_once_with(component, input_class_name)  # noqa

    mock_update_enum.assert_called_once_with(component, input_class_alias, with_file_update=True)  # noqa
    mock_create_config_model.assert_called_once_with(component, mock_class, input_config_model_name, with_file_update=True)  # noqa
    mock_update_factory.assert_called_once_with(component, input_module_name, input_class_name, input_class_alias, input_config_model_name, with_file_update=True)  # noqa
    mock_update_subpackage_init.assert_called_once_with(component, input_module_name, with_file_update=True)  # noqa
    mock_update_test_of_factory.assert_called_once_with(component, input_module_name, input_class_name, input_class_alias, input_config_model_name, with_file_update=True)  # noqa
