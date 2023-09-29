import simple_typing_application
from .enum import EComponent

COMPONENT_NAME_MAP: dict[EComponent, str] = {
    EComponent.KEY_MONITOR: 'key_monitor',
    EComponent.SENTENCE_GENERATOR: 'sentence_generator',
    EComponent.UI: 'user_interface',
}
COMPONENT_ENUMNAME_MAP: dict[EComponent, str] = {
    EComponent.KEY_MONITOR: simple_typing_application.const.key_monitor.EKeyMonitorType.__name__,  # noqa
    EComponent.SENTENCE_GENERATOR: simple_typing_application.const.sentence_generator.ESentenceGeneratorType.__name__,  # noqa
    EComponent.UI: simple_typing_application.const.user_interface.EUserInterfaceType.__name__,  # noqa
}

COMPONENT_BASE_CONFIG_MODEL_MAP: dict[EComponent, str] = {
    EComponent.KEY_MONITOR: simple_typing_application.models.config_models.key_monitor_config_model.BaseKeyMonitorConfigModel.__name__,  # noqa
    EComponent.SENTENCE_GENERATOR: simple_typing_application.models.config_models.sentence_generator_config_model.BaseSentenceGeneratorConfigModel.__name__,  # noqa
    EComponent.UI: simple_typing_application.models.config_models.user_interface_config_model.BaseUserInterfaceConfigModel.__name__,  # noqa
}
PACKAGE: str = simple_typing_application.__name__
PACKAGE_DIR: str = simple_typing_application.__path__[0]
COMPONENT_SUBPACKAGE_MAP = {
    EComponent.KEY_MONITOR: simple_typing_application.key_monitor.__name__,
    EComponent.SENTENCE_GENERATOR: simple_typing_application.sentence_generator.__name__,  # noqa
    EComponent.UI: simple_typing_application.ui.__name__,
}
COMPONENT_SUBPACKAGE_DIR_MAP = {
    EComponent.KEY_MONITOR: simple_typing_application.key_monitor.__path__[0],
    EComponent.SENTENCE_GENERATOR: simple_typing_application.sentence_generator.__path__[0],  # noqa
    EComponent.UI: simple_typing_application.ui.__path__[0],
}
