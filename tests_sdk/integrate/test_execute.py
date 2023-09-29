import os
import pytest
from sdk.const import (
    PACKAGE_DIR,
    COMPONENT_NAME_MAP,
    COMPONENT_SUBPACKAGE_DIR_MAP,
)
from sdk.enum import EComponent
from sdk.integrate.execute import (
    update_enum,
    create_config_model,
    update_factory,
    update_subpackage_init,
    update_test_of_factory,
)


@pytest.mark.sdk
@pytest.mark.parametrize(
    'component, class_alias, current_enum, expected_enum',
    [
        (
            EComponent.KEY_MONITOR,
            'NEW_KEY_MONITOR',
            """from enum import Enum


class EKeyMonitorType(Enum):
    PYNPUT: str = 'PYNPUT'""",
            """from enum import Enum


class EKeyMonitorType(Enum):
    NEW_KEY_MONITOR: str = 'NEW_KEY_MONITOR'
    PYNPUT: str = 'PYNPUT'""",
        ),
        (
            EComponent.UI,
            'NEW_UI',
            """from enum import Enum


class EUserInterfaceType(Enum):
    CONSOLE: str = 'CONSOLE'""",
            """from enum import Enum


class EUserInterfaceType(Enum):
    NEW_UI: str = 'NEW_UI'
    CONSOLE: str = 'CONSOLE'""",
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            'NEW_SENTENCE_GENERATOR',
            """from enum import Enum


class ESentenceGeneratorType(Enum):
    OPENAI: str = 'OPENAI'
    HUGGINGFACE: str = 'HUGGINGFACE'
    STATIC: str = 'STATIC'""",
            """from enum import Enum


class ESentenceGeneratorType(Enum):
    NEW_SENTENCE_GENERATOR: str = 'NEW_SENTENCE_GENERATOR'
    OPENAI: str = 'OPENAI'
    HUGGINGFACE: str = 'HUGGINGFACE'
    STATIC: str = 'STATIC'""",
        ),
    ],
)
def test_update_enum(
    component: EComponent,
    class_alias: str,
    current_enum: str,
    expected_enum: str,
    mocker,
):
    # mock
    mock_open = mocker.patch('builtins.open', new_callable=mocker.mock_open)  # noqa
    mock_open().read.return_value = current_enum

    # execute
    actual = update_enum(component, class_alias, with_file_update=False)  # noqa
    # assert
    assert actual == expected_enum
    mock_open.assert_called_with(
        os.path.join(
            PACKAGE_DIR,
            'const',
            f'{COMPONENT_NAME_MAP[component]}.py',
        ),
        'r',
        encoding='utf-8',
    )
    mock_open().write.assert_not_called()

    # execute with file update
    actual = update_enum(component, class_alias, with_file_update=True)  # noqa
    # assert
    assert actual == expected_enum
    mock_open().write.assert_called_once_with(expected_enum)


def dummy_init1(self, hoge: str, fuga, piyo=1, hogehoge: int = 2):
    pass


def dummy_init2(self, hoge: str, *args, fuga: int = 2, **kwargs):
    pass


def dummy_init3(self, *args, **kwargs):
    pass


@pytest.mark.sdk
@pytest.mark.parametrize(
    'component, created_class, config_model_name, current_config_model, expected_config_model',  # noqa
    [
        (
            EComponent.KEY_MONITOR,
            type('NewKeyMonitor', (object,), dict(__init__=dummy_init1)),
            'NewKeyMonitorConfigModel',
            """from pydantic import BaseModel


class BaseKeyMonitorConfigModel(BaseModel):
    pass


class PynputBasedKeyMonitorConfigModel(BaseKeyMonitorConfigModel):
    pass
""",
            """from pydantic import BaseModel


class BaseKeyMonitorConfigModel(BaseModel):
    pass


class PynputBasedKeyMonitorConfigModel(BaseKeyMonitorConfigModel):
    pass


class NewKeyMonitorConfigModel(BaseKeyMonitorConfigModel):
    hoge: str
    fuga
    piyo = 1
    hogehoge: int = 2
""",
        ),
        (
            EComponent.UI,
            type('NewUI', (object,), dict(__init__=dummy_init2)),
            'NewUIConfigModel',
            """from pydantic import BaseModel


class BaseUserInterfaceConfigModel(BaseModel):
    pass


class ConsoleUserInterfaceConfigModel(BaseUserInterfaceConfigModel):
    pass
""",
            """from pydantic import BaseModel


class BaseUserInterfaceConfigModel(BaseModel):
    pass


class ConsoleUserInterfaceConfigModel(BaseUserInterfaceConfigModel):
    pass


class NewUIConfigModel(BaseUserInterfaceConfigModel):
    hoge: str
    fuga: int = 2
""",
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            type('NewSentenceGenerator', (object,), dict(__init__=dummy_init3)),  # noqa
            'NewSentenceGeneratorConfigModel',
            """from pydantic import BaseModel


class BaseSentenceGeneratorConfigModel(BaseModel):
    pass


class OpenAISentenceGeneratorConfigModel(BaseSentenceGeneratorConfigModel):
    model: str = 'gpt-3.5-turbo-16k'
    temperature: float = 0.7
    openai_api_key: str | None = None
    memory_size: int = 0
    max_retry: int = 5
""",
            """from pydantic import BaseModel


class BaseSentenceGeneratorConfigModel(BaseModel):
    pass


class OpenAISentenceGeneratorConfigModel(BaseSentenceGeneratorConfigModel):
    model: str = 'gpt-3.5-turbo-16k'
    temperature: float = 0.7
    openai_api_key: str | None = None
    memory_size: int = 0
    max_retry: int = 5


class NewSentenceGeneratorConfigModel(BaseSentenceGeneratorConfigModel):
    pass
"""
        )
    ],
)
def test_create_config_model(
    component: EComponent,
    created_class: type,
    config_model_name: str,
    current_config_model: str,
    expected_config_model: str,
    mocker
):
    # mock
    mock_open = mocker.patch('builtins.open', new_callable=mocker.mock_open)  # noqa
    mock_open().read.return_value = current_config_model

    # execute without file update
    actual = create_config_model(
        component,
        created_class,
        config_model_name,
        with_file_update=False,
    )
    # assert
    assert actual == expected_config_model
    mock_open.assert_called_with(
        os.path.join(
            PACKAGE_DIR,
            'models',
            'config_models',
            f'{COMPONENT_NAME_MAP[component]}_config_model.py',
        ),
        'r',
        encoding='utf-8',
    )
    mock_open().write.assert_not_called()

    # execute with file update
    actual = create_config_model(
        component,
        created_class,
        config_model_name,
        with_file_update=True,
    )
    # assert
    assert actual == expected_config_model
    mock_open().write.assert_called_once_with(expected_config_model)


@pytest.mark.sdk
@pytest.mark.parametrize(
    'component, module_name, class_name, class_alias, config_model_name, current_factory, expected_factory',  # noqa
    [
        (
            EComponent.KEY_MONITOR,
            'new_key_monitor',
            'NewKeyMonitor',
            'NEW_KEY_MONITOR',
            'NewKeyMonitorConfigModel',
            """from logging import getLogger, Logger


from .base import BaseKeyMonitor
from .pynput import PynputBasedKeyMonitor
from ..const.key_monitor import EKeyMonitorType
from ..models.config_models.key_monitor_config_model import (
    BaseKeyMonitorConfigModel,
    PynputBasedKeyMonitorConfigModel,
)


def _select_class_and_config_model(key_monitor_type: EKeyMonitorType) -> tuple[type, type]:  # noqa

    if key_monitor_type == EKeyMonitorType.PYNPUT:
        return PynputBasedKeyMonitor, PynputBasedKeyMonitorConfigModel
    else:
        raise ValueError(f'Unsupported key monitor type: {key_monitor_type}')


def create_key_monitor(
    key_monitor_type: EKeyMonitorType,
    dict_config: dict[str, str | float | int | bool | None | dict | list],
    logger: Logger = getLogger(__name__),
) -> BaseKeyMonitor:

    # select key monitor class and config model
    try:
        key_monitor_cls, key_monitor_config_model = _select_class_and_config_model(key_monitor_type)  # noqa
    except NameError:
        raise ImportError(f'Failed to import key monitor class and config model for key_monitor_type={key_monitor_type}')  # noqa

    # create key monitor
    logger.debug(f'create {key_monitor_cls.__name__}')
    key_monitor_config: BaseKeyMonitorConfigModel = key_monitor_config_model(**dict_config)  # noqa
    key_monitor: BaseKeyMonitor = key_monitor_cls(**key_monitor_config.model_dump())    # type: ignore # noqa

    return key_monitor
""",
            """from logging import getLogger, Logger


from .base import BaseKeyMonitor
from .pynput import PynputBasedKeyMonitor
from .new_key_monitor import NewKeyMonitor
from ..const.key_monitor import EKeyMonitorType
from ..models.config_models.key_monitor_config_model import (
    NewKeyMonitorConfigModel,
    BaseKeyMonitorConfigModel,
    PynputBasedKeyMonitorConfigModel,
)


def _select_class_and_config_model(key_monitor_type: EKeyMonitorType) -> tuple[type, type]:  # noqa

    if key_monitor_type == EKeyMonitorType.PYNPUT:
        return PynputBasedKeyMonitor, PynputBasedKeyMonitorConfigModel
    elif key_monitor_type == EKeyMonitorType.NEW_KEY_MONITOR:
        return NewKeyMonitor, NewKeyMonitorConfigModel
    else:
        raise ValueError(f'Unsupported key monitor type: {key_monitor_type}')


def create_key_monitor(
    key_monitor_type: EKeyMonitorType,
    dict_config: dict[str, str | float | int | bool | None | dict | list],
    logger: Logger = getLogger(__name__),
) -> BaseKeyMonitor:

    # select key monitor class and config model
    try:
        key_monitor_cls, key_monitor_config_model = _select_class_and_config_model(key_monitor_type)  # noqa
    except NameError:
        raise ImportError(f'Failed to import key monitor class and config model for key_monitor_type={key_monitor_type}')  # noqa

    # create key monitor
    logger.debug(f'create {key_monitor_cls.__name__}')
    key_monitor_config: BaseKeyMonitorConfigModel = key_monitor_config_model(**dict_config)  # noqa
    key_monitor: BaseKeyMonitor = key_monitor_cls(**key_monitor_config.model_dump())    # type: ignore # noqa

    return key_monitor
"""
        ),
        (
            EComponent.UI,
            'new_ui',
            'NewUI',
            'NEW_UI',
            'NewUIConfigModel',
            """from logging import getLogger, Logger

from .base import BaseUserInterface
from .cui import ConsoleUserInterface
from ..const.user_interface import EUserInterfaceType
from ..models.config_models.user_interface_config_model import (  # noqa
    BaseUserInterfaceConfigModel,
    ConsoleUserInterfaceConfigModel,
)


def _select_class_and_config_model(user_interface_type: EUserInterfaceType) -> tuple[type, type]:  # noqa

    if user_interface_type == EUserInterfaceType.CONSOLE:
        return ConsoleUserInterface, ConsoleUserInterfaceConfigModel
    else:
        raise ValueError(f'Unsupported user interface type: {user_interface_type}')  # noqa


def create_user_interface(
    user_interface_type: EUserInterfaceType,
    dict_config: dict[str, str | float | int | bool | None | dict | list],
    logger: Logger = getLogger(__name__),
) -> BaseUserInterface:

    # select user interface class and config model
    try:
        user_interface_cls, user_interface_config_model = _select_class_and_config_model(user_interface_type)  # noqa
    except NameError:
        raise ImportError(f'Failed to import user interface class and config model for user_interface_type={user_interface_type}')  # noqa

    # create user interface
    logger.debug(f'create {user_interface_cls.__name__}')
    user_interface_config: BaseUserInterfaceConfigModel = user_interface_config_model(**dict_config)  # noqa
    user_interface: BaseUserInterface = user_interface_cls(**user_interface_config.model_dump())    # type: ignore # noqa

    return user_interface
""",
            """from logging import getLogger, Logger

from .base import BaseUserInterface
from .cui import ConsoleUserInterface
from .new_ui import NewUI
from ..const.user_interface import EUserInterfaceType
from ..models.config_models.user_interface_config_model import (  # noqa
    NewUIConfigModel,
    BaseUserInterfaceConfigModel,
    ConsoleUserInterfaceConfigModel,
)


def _select_class_and_config_model(user_interface_type: EUserInterfaceType) -> tuple[type, type]:  # noqa

    if user_interface_type == EUserInterfaceType.CONSOLE:
        return ConsoleUserInterface, ConsoleUserInterfaceConfigModel
    elif user_interface_type == EUserInterfaceType.NEW_UI:
        return NewUI, NewUIConfigModel
    else:
        raise ValueError(f'Unsupported user interface type: {user_interface_type}')  # noqa


def create_user_interface(
    user_interface_type: EUserInterfaceType,
    dict_config: dict[str, str | float | int | bool | None | dict | list],
    logger: Logger = getLogger(__name__),
) -> BaseUserInterface:

    # select user interface class and config model
    try:
        user_interface_cls, user_interface_config_model = _select_class_and_config_model(user_interface_type)  # noqa
    except NameError:
        raise ImportError(f'Failed to import user interface class and config model for user_interface_type={user_interface_type}')  # noqa

    # create user interface
    logger.debug(f'create {user_interface_cls.__name__}')
    user_interface_config: BaseUserInterfaceConfigModel = user_interface_config_model(**dict_config)  # noqa
    user_interface: BaseUserInterface = user_interface_cls(**user_interface_config.model_dump())    # type: ignore # noqa

    return user_interface
"""
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            'new_sentence_generator',
            'NewSentenceGenerator',
            'NEW_SENTENCE_GENERATOR',
            'NewSentenceGeneratorConfigModel',
            """import logging
from logging import getLogger, Logger

from .base import BaseSentenceGenerator  # noqa
try:
    from .huggingface_sentence_generator import HuggingfaceSentenceGenerator  # noqa
except ImportError:
    logging.warning(
        'Failed to import HuggingfaceSentenceGenerator. '
        'If you want to use HuggingfaceSentenceGenerator, `pip install simple_typing_application[huggingface]`.'  # noqa
    )
from .openai_sentence_generator import OpenaiSentenceGenerator  # noqa
from .static_sentence_generator import StaticSentenceGenerator  # noqa
from ..const.sentence_generator import ESentenceGeneratorType  # noqa
from ..models.config_models.sentence_generator_config_model import (  # noqa
    BaseSentenceGeneratorConfigModel,
    OpenAISentenceGeneratorConfigModel,
    HuggingfaceSentenceGeneratorConfigModel,
    StaticSentenceGeneratorConfigModel,
)


def _select_class_and_config_model(sentence_generator_type: ESentenceGeneratorType) -> tuple[type, type]:  # noqa

    if sentence_generator_type == ESentenceGeneratorType.OPENAI:
        return OpenaiSentenceGenerator, OpenAISentenceGeneratorConfigModel
    elif sentence_generator_type == ESentenceGeneratorType.HUGGINGFACE:
        return HuggingfaceSentenceGenerator, HuggingfaceSentenceGeneratorConfigModel  # noqa
    elif sentence_generator_type == ESentenceGeneratorType.STATIC:
        return StaticSentenceGenerator, StaticSentenceGeneratorConfigModel
    else:
        raise ValueError(f'Unsupported sentence generator type: {sentence_generator_type}')  # noqa


def create_sentence_generator(
    sentence_generator_type: ESentenceGeneratorType,
    dict_config: dict[str, str | float | int | bool | None | dict | list],
    logger: Logger = getLogger(__name__),
) -> BaseSentenceGenerator:

    # select sentence generator class and config model
    try:
        sentence_generator_cls, sentence_generator_config_model = _select_class_and_config_model(sentence_generator_type)  # noqa
    except NameError:
        raise ImportError(f'Failed to import sentence generator class and config model for sentence_generator_type={sentence_generator_type}')  # noqa

    # create sentence generator
    logger.debug(f'create {sentence_generator_cls.__name__}')
    sentence_generator_config: BaseSentenceGeneratorConfigModel = sentence_generator_config_model(**dict_config)  # noqa
    sentence_generator: BaseSentenceGenerator = sentence_generator_cls(**sentence_generator_config.model_dump())    # type: ignore # noqa

    return sentence_generator
""",
            """import logging
from logging import getLogger, Logger

from .base import BaseSentenceGenerator  # noqa
try:
    from .huggingface_sentence_generator import HuggingfaceSentenceGenerator  # noqa
except ImportError:
    logging.warning(
        'Failed to import HuggingfaceSentenceGenerator. '
        'If you want to use HuggingfaceSentenceGenerator, `pip install simple_typing_application[huggingface]`.'  # noqa
    )
from .openai_sentence_generator import OpenaiSentenceGenerator  # noqa
from .static_sentence_generator import StaticSentenceGenerator  # noqa
from .new_sentence_generator import NewSentenceGenerator
from ..const.sentence_generator import ESentenceGeneratorType  # noqa
from ..models.config_models.sentence_generator_config_model import (  # noqa
    NewSentenceGeneratorConfigModel,
    BaseSentenceGeneratorConfigModel,
    OpenAISentenceGeneratorConfigModel,
    HuggingfaceSentenceGeneratorConfigModel,
    StaticSentenceGeneratorConfigModel,
)


def _select_class_and_config_model(sentence_generator_type: ESentenceGeneratorType) -> tuple[type, type]:  # noqa

    if sentence_generator_type == ESentenceGeneratorType.OPENAI:
        return OpenaiSentenceGenerator, OpenAISentenceGeneratorConfigModel
    elif sentence_generator_type == ESentenceGeneratorType.HUGGINGFACE:
        return HuggingfaceSentenceGenerator, HuggingfaceSentenceGeneratorConfigModel  # noqa
    elif sentence_generator_type == ESentenceGeneratorType.STATIC:
        return StaticSentenceGenerator, StaticSentenceGeneratorConfigModel
    elif sentence_generator_type == ESentenceGeneratorType.NEW_SENTENCE_GENERATOR:
        return NewSentenceGenerator, NewSentenceGeneratorConfigModel
    else:
        raise ValueError(f'Unsupported sentence generator type: {sentence_generator_type}')  # noqa


def create_sentence_generator(
    sentence_generator_type: ESentenceGeneratorType,
    dict_config: dict[str, str | float | int | bool | None | dict | list],
    logger: Logger = getLogger(__name__),
) -> BaseSentenceGenerator:

    # select sentence generator class and config model
    try:
        sentence_generator_cls, sentence_generator_config_model = _select_class_and_config_model(sentence_generator_type)  # noqa
    except NameError:
        raise ImportError(f'Failed to import sentence generator class and config model for sentence_generator_type={sentence_generator_type}')  # noqa

    # create sentence generator
    logger.debug(f'create {sentence_generator_cls.__name__}')
    sentence_generator_config: BaseSentenceGeneratorConfigModel = sentence_generator_config_model(**dict_config)  # noqa
    sentence_generator: BaseSentenceGenerator = sentence_generator_cls(**sentence_generator_config.model_dump())    # type: ignore # noqa

    return sentence_generator
"""
        )
    ]
)
def test_update_factory(
    component: EComponent,
    module_name: str,
    class_name: str,
    class_alias: str,
    config_model_name: str,
    current_factory: str,
    expected_factory: str,
    mocker,
):
    # mock
    mock_open = mocker.patch('builtins.open', new_callable=mocker.mock_open)  # noqa
    mock_open().read.return_value = current_factory

    # execute without file update
    actual = update_factory(
        component,
        module_name,
        class_name,
        class_alias,
        config_model_name,
        with_file_update=False,
    )
    # assert
    assert actual == expected_factory
    mock_open.assert_called_with(
        os.path.join(
            COMPONENT_SUBPACKAGE_DIR_MAP[component],
            'factory.py',
        ),
        'r',
        encoding='utf-8',
    )
    mock_open().write.assert_not_called()

    # execute with file update
    actual = update_factory(
        component,
        module_name,
        class_name,
        class_alias,
        config_model_name,
        with_file_update=True,
    )
    # assert
    assert actual == expected_factory
    mock_open().write.assert_called_once_with(expected_factory)


@pytest.mark.sdk
@pytest.mark.parametrize(
    'component, module_name, current_init, expected_init',
    [
        (
            EComponent.KEY_MONITOR,
            'new_key_monitor',
            """from . import (
    base,
    factory,
    pynput,
)
from .base import BaseKeyMonitor
from .factory import create_key_monitor
from .pynput import PynputBasedKeyMonitor


__all__ = [
    base.__name__,
    factory.__name__,
    pynput.__name__,
    BaseKeyMonitor.__name__,
    create_key_monitor.__name__,
    PynputBasedKeyMonitor.__name__,
]
""",
            """from . import (
    new_key_monitor,
    base,
    factory,
    pynput,
)
from .base import BaseKeyMonitor
from .factory import create_key_monitor
from .pynput import PynputBasedKeyMonitor


__all__ = [
    base.__name__,
    new_key_monitor.__name__,
    factory.__name__,
    pynput.__name__,
    BaseKeyMonitor.__name__,
    create_key_monitor.__name__,
    PynputBasedKeyMonitor.__name__,
]
""",
        ),
        (
            EComponent.UI,
            'new_ui',
            """from . import (
    base,
    factory,
    cui,
)

from .base import BaseUserInterface
from .cui import ConsoleUserInterface
from .factory import create_user_interface


__all__ = [
    base.__name__,
    factory.__name__,
    cui.__name__,

    BaseUserInterface.__name__,
    ConsoleUserInterface.__name__,
    create_user_interface.__name__,
]
""",
            """from . import (
    new_ui,
    base,
    factory,
    cui,
)

from .base import BaseUserInterface
from .cui import ConsoleUserInterface
from .factory import create_user_interface


__all__ = [
    base.__name__,
    new_ui.__name__,
    factory.__name__,
    cui.__name__,

    BaseUserInterface.__name__,
    ConsoleUserInterface.__name__,
    create_user_interface.__name__,
]
""",
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            'new_sentence_generator',
            """from . import (
    base,
    factory,
    openai_sentence_generator,
    huggingface_sentence_generator,
    static_sentence_generator,
    utils,
)

from .base import BaseSentenceGenerator
from .factory import create_sentence_generator
from .openai_sentence_generator import OpenaiSentenceGenerator


__all__ = [
    base.__name__,
    factory.__name__,
    openai_sentence_generator.__name__,
    huggingface_sentence_generator.__name__,
    static_sentence_generator.__name__,
    utils.__name__,

    BaseSentenceGenerator.__name__,
    create_sentence_generator.__name__,
    OpenaiSentenceGenerator.__name__,
]
""",
            """from . import (
    new_sentence_generator,
    base,
    factory,
    openai_sentence_generator,
    huggingface_sentence_generator,
    static_sentence_generator,
    utils,
)

from .base import BaseSentenceGenerator
from .factory import create_sentence_generator
from .openai_sentence_generator import OpenaiSentenceGenerator


__all__ = [
    base.__name__,
    new_sentence_generator.__name__,
    factory.__name__,
    openai_sentence_generator.__name__,
    huggingface_sentence_generator.__name__,
    static_sentence_generator.__name__,
    utils.__name__,

    BaseSentenceGenerator.__name__,
    create_sentence_generator.__name__,
    OpenaiSentenceGenerator.__name__,
]
""",
        )
    ]
)
def test_update_subpackage_init(
    component: EComponent,
    module_name: str,
    current_init: str,
    expected_init: str,
    mocker,
):
    # mock
    mock_open = mocker.patch('builtins.open', new_callable=mocker.mock_open)
    mock_open().read.return_value = current_init

    # execute without file update
    actual = update_subpackage_init(
        component,
        module_name,
        with_file_update=False,
    )
    # assert
    assert actual == expected_init
    mock_open.assert_called_with(
        os.path.join(
            COMPONENT_SUBPACKAGE_DIR_MAP[component],
            '__init__.py',
        ),
        'r',
        encoding='utf-8',
    )
    mock_open().write.assert_not_called()

    # execute with file update
    actual = update_subpackage_init(
        component,
        module_name,
        with_file_update=True,
    )
    # assert
    assert actual == expected_init
    mock_open().write.assert_called_once_with(expected_init)


@pytest.mark.sdk
@pytest.mark.parametrize(
    'component, module_name, class_name, class_alias, config_model_name, current_test, expected_test',  # noqa
    [
        (
            EComponent.KEY_MONITOR,
            'new_key_monitor',
            'NewKeyMonitor',
            'NEW_KEY_MONITOR',
            'NewKeyMonitorConfigModel',
            """import pytest

from simple_typing_application.const.key_monitor import EKeyMonitorType  # noqa
from simple_typing_application.models.config_models.key_monitor_config_model import (  # noqa
    PynputBasedKeyMonitorConfigModel,
)
from simple_typing_application.key_monitor.factory import (
    create_key_monitor,
    _select_class_and_config_model
)
from simple_typing_application.key_monitor.pynput import PynputBasedKeyMonitor  # noqa


@pytest.mark.parametrize(
    "key_monitor_type, expected_class, expected_config_model",
    [
        (EKeyMonitorType.PYNPUT, PynputBasedKeyMonitor, PynputBasedKeyMonitorConfigModel),  # noqa
    ]
)
def test_select_class_and_config_model(
    key_monitor_type: EKeyMonitorType,
    expected_class: type,
    expected_config_model: type,
):
    ...


@pytest.mark.parametrize(
    "key_monitor_type, key_monitor_config_dict, expected_class",
    [
        (
            EKeyMonitorType.PYNPUT,
            PynputBasedKeyMonitorConfigModel().model_dump(),
            PynputBasedKeyMonitor,
        ),
        (
            EKeyMonitorType.PYNPUT,
            {},
            PynputBasedKeyMonitor,
        ),
    ]
)
def test_create_key_monitor(
    key_monitor_type: EKeyMonitorType,
    key_monitor_config_dict: dict[str, str | float | int | bool | None | dict | list],  # noqa
    expected_class: type,
    mocker,
):
    ...
""",
            """import pytest

from simple_typing_application.const.key_monitor import EKeyMonitorType  # noqa
from simple_typing_application.models.config_models.key_monitor_config_model import (  # noqa
    NewKeyMonitorConfigModel,
    PynputBasedKeyMonitorConfigModel,
)
from simple_typing_application.key_monitor.new_key_monitor import NewKeyMonitor  # noqa
from simple_typing_application.key_monitor.factory import (
    create_key_monitor,
    _select_class_and_config_model
)
from simple_typing_application.key_monitor.pynput import PynputBasedKeyMonitor  # noqa


@pytest.mark.parametrize(
    "key_monitor_type, expected_class, expected_config_model",
    [
        (EKeyMonitorType.PYNPUT, PynputBasedKeyMonitor, PynputBasedKeyMonitorConfigModel),  # noqa
        (EKeyMonitorType.NEW_KEY_MONITOR, NewKeyMonitor, NewKeyMonitorConfigModel),  # noqa
    ]
)
def test_select_class_and_config_model(
    key_monitor_type: EKeyMonitorType,
    expected_class: type,
    expected_config_model: type,
):
    ...


@pytest.mark.parametrize(
    "key_monitor_type, key_monitor_config_dict, expected_class",
    [
        (
            EKeyMonitorType.PYNPUT,
            PynputBasedKeyMonitorConfigModel().model_dump(),
            PynputBasedKeyMonitor,
        ),
        (
            EKeyMonitorType.PYNPUT,
            {},
            PynputBasedKeyMonitor,
        ),
        (EKeyMonitorType.NEW_KEY_MONITOR, NewKeyMonitorConfigModel().model_dump(), NewKeyMonitor),  # noqa
    ]
)
def test_create_key_monitor(
    key_monitor_type: EKeyMonitorType,
    key_monitor_config_dict: dict[str, str | float | int | bool | None | dict | list],  # noqa
    expected_class: type,
    mocker,
):
    ...
""",
        ),
        (
            EComponent.UI,
            'new_ui',
            'NewUI',
            'NEW_UI',
            'NewUIConfigModel',
            """import pytest

from simple_typing_application.const.user_interface import EUserInterfaceType
from simple_typing_application.models.config_models.user_interface_config_model import (  # noqa
    ConsoleUserInterfaceConfigModel,
)
from simple_typing_application.ui.cui import ConsoleUserInterface
from simple_typing_application.ui.factory import (
    create_user_interface,
    _select_class_and_config_model,
)


@pytest.mark.parametrize(
    'user_interface_type, expected_class, expected_config_model',
    [
        (
            EUserInterfaceType.CONSOLE,
            ConsoleUserInterface,
            ConsoleUserInterfaceConfigModel,
        ),
    ],
)
def test_select_class_and_config_model(
    user_interface_type: EUserInterfaceType,
    expected_class: type,
    expected_config_model: type,
):
    ...


@pytest.mark.parametrize(
    'user_interface_type, user_interface_config_dict, expected_class',
    [
        (
            EUserInterfaceType.CONSOLE,
            ConsoleUserInterfaceConfigModel().model_dump(),
            ConsoleUserInterface,
        ),
        (
            EUserInterfaceType.CONSOLE,
            {},
            ConsoleUserInterface,
        ),
    ],
)
def test_create_user_interface(
    user_interface_type: EUserInterfaceType,
    user_interface_config_dict: dict[str, str | float | int | bool | None | dict | list],  # noqa
    expected_class: type,
    mocker,
):
    ...
""",
            """import pytest

from simple_typing_application.const.user_interface import EUserInterfaceType
from simple_typing_application.models.config_models.user_interface_config_model import (  # noqa
    NewUIConfigModel,
    ConsoleUserInterfaceConfigModel,
)
from simple_typing_application.ui.cui import ConsoleUserInterface
from simple_typing_application.ui.new_ui import NewUI  # noqa
from simple_typing_application.ui.factory import (
    create_user_interface,
    _select_class_and_config_model,
)


@pytest.mark.parametrize(
    'user_interface_type, expected_class, expected_config_model',
    [
        (
            EUserInterfaceType.CONSOLE,
            ConsoleUserInterface,
            ConsoleUserInterfaceConfigModel,
        ),
        (EUserInterfaceType.NEW_UI, NewUI, NewUIConfigModel),  # noqa
    ],
)
def test_select_class_and_config_model(
    user_interface_type: EUserInterfaceType,
    expected_class: type,
    expected_config_model: type,
):
    ...


@pytest.mark.parametrize(
    'user_interface_type, user_interface_config_dict, expected_class',
    [
        (
            EUserInterfaceType.CONSOLE,
            ConsoleUserInterfaceConfigModel().model_dump(),
            ConsoleUserInterface,
        ),
        (
            EUserInterfaceType.CONSOLE,
            {},
            ConsoleUserInterface,
        ),
        (EUserInterfaceType.NEW_UI, NewUIConfigModel().model_dump(), NewUI),  # noqa
    ],
)
def test_create_user_interface(
    user_interface_type: EUserInterfaceType,
    user_interface_config_dict: dict[str, str | float | int | bool | None | dict | list],  # noqa
    expected_class: type,
    mocker,
):
    ...
""",
        ),
        (
            EComponent.SENTENCE_GENERATOR,
            'new_sentence_generator',
            'NewSentenceGenerator',
            'NEW_SENTENCE_GENERATOR',
            'NewSentenceGeneratorConfigModel',
            """import pytest

from simple_typing_application.const.sentence_generator import ESentenceGeneratorType  # noqa
from simple_typing_application.models.config_models.sentence_generator_config_model import (  # noqa
    OpenAISentenceGeneratorConfigModel,
    HuggingfaceSentenceGeneratorConfigModel,
    StaticSentenceGeneratorConfigModel,
)
from simple_typing_application.sentence_generator.factory import (
    create_sentence_generator,
    _select_class_and_config_model,
)
from simple_typing_application.sentence_generator.huggingface_sentence_generator import HuggingfaceSentenceGenerator  # noqa
from simple_typing_application.sentence_generator.openai_sentence_generator import OpenaiSentenceGenerator  # noqa
from simple_typing_application.sentence_generator.static_sentence_generator import StaticSentenceGenerator  # noqa


@pytest.mark.parametrize(
    "sentence_generator_type, expected_class, expected_config_model",
    [
        (
            ESentenceGeneratorType.OPENAI,
            OpenaiSentenceGenerator,
            OpenAISentenceGeneratorConfigModel,
        ),
        (
            ESentenceGeneratorType.HUGGINGFACE,
            HuggingfaceSentenceGenerator,
            HuggingfaceSentenceGeneratorConfigModel,
        ),
        (
            ESentenceGeneratorType.STATIC,
            StaticSentenceGenerator,
            StaticSentenceGeneratorConfigModel,
        ),
    ]
)
def test_select_class_and_config_model(
    sentence_generator_type: ESentenceGeneratorType,
    expected_class: type,
    expected_config_model: type,
):
    ...


@pytest.mark.parametrize(
    "sentence_generator_type, sentence_generator_config_dict, expected_class",
    [
        (
            ESentenceGeneratorType.OPENAI,
            OpenAISentenceGeneratorConfigModel().model_dump(),
            OpenaiSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.HUGGINGFACE,
            HuggingfaceSentenceGeneratorConfigModel().model_dump(),
            HuggingfaceSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.STATIC,
            StaticSentenceGeneratorConfigModel(text_kana_map={}).model_dump(),
            StaticSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.OPENAI,
            {},
            OpenaiSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.HUGGINGFACE,
            {},
            HuggingfaceSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.STATIC,
            {},
            StaticSentenceGenerator,
        ),
    ]
)
def test_create_sentence_generator(
    sentence_generator_type: ESentenceGeneratorType,
    sentence_generator_config_dict: dict[str, str | float | int | bool | None | dict | list],  # noqa
    expected_class: type,
    mocker,
):
    ...
""",
            """import pytest

from simple_typing_application.const.sentence_generator import ESentenceGeneratorType  # noqa
from simple_typing_application.models.config_models.sentence_generator_config_model import (  # noqa
    NewSentenceGeneratorConfigModel,
    OpenAISentenceGeneratorConfigModel,
    HuggingfaceSentenceGeneratorConfigModel,
    StaticSentenceGeneratorConfigModel,
)
from simple_typing_application.sentence_generator.new_sentence_generator import NewSentenceGenerator  # noqa
from simple_typing_application.sentence_generator.factory import (
    create_sentence_generator,
    _select_class_and_config_model,
)
from simple_typing_application.sentence_generator.huggingface_sentence_generator import HuggingfaceSentenceGenerator  # noqa
from simple_typing_application.sentence_generator.openai_sentence_generator import OpenaiSentenceGenerator  # noqa
from simple_typing_application.sentence_generator.static_sentence_generator import StaticSentenceGenerator  # noqa


@pytest.mark.parametrize(
    "sentence_generator_type, expected_class, expected_config_model",
    [
        (
            ESentenceGeneratorType.OPENAI,
            OpenaiSentenceGenerator,
            OpenAISentenceGeneratorConfigModel,
        ),
        (
            ESentenceGeneratorType.HUGGINGFACE,
            HuggingfaceSentenceGenerator,
            HuggingfaceSentenceGeneratorConfigModel,
        ),
        (
            ESentenceGeneratorType.STATIC,
            StaticSentenceGenerator,
            StaticSentenceGeneratorConfigModel,
        ),
        (ESentenceGeneratorType.NEW_SENTENCE_GENERATOR, NewSentenceGenerator, NewSentenceGeneratorConfigModel),  # noqa
    ]
)
def test_select_class_and_config_model(
    sentence_generator_type: ESentenceGeneratorType,
    expected_class: type,
    expected_config_model: type,
):
    ...


@pytest.mark.parametrize(
    "sentence_generator_type, sentence_generator_config_dict, expected_class",
    [
        (
            ESentenceGeneratorType.OPENAI,
            OpenAISentenceGeneratorConfigModel().model_dump(),
            OpenaiSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.HUGGINGFACE,
            HuggingfaceSentenceGeneratorConfigModel().model_dump(),
            HuggingfaceSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.STATIC,
            StaticSentenceGeneratorConfigModel(text_kana_map={}).model_dump(),
            StaticSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.OPENAI,
            {},
            OpenaiSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.HUGGINGFACE,
            {},
            HuggingfaceSentenceGenerator,
        ),
        (
            ESentenceGeneratorType.STATIC,
            {},
            StaticSentenceGenerator,
        ),
        (ESentenceGeneratorType.NEW_SENTENCE_GENERATOR, NewSentenceGeneratorConfigModel().model_dump(), NewSentenceGenerator),  # noqa
    ]
)
def test_create_sentence_generator(
    sentence_generator_type: ESentenceGeneratorType,
    sentence_generator_config_dict: dict[str, str | float | int | bool | None | dict | list],  # noqa
    expected_class: type,
    mocker,
):
    ...
"""
        )
    ]
)
def test_update_test_of_factory(
    component: EComponent,
    module_name: str,
    class_name: str,
    class_alias: str,
    config_model_name: str,
    current_test: str,
    expected_test: str,
    mocker,
):
    # mock
    mock_open = mocker.patch('builtins.open', new_callable=mocker.mock_open)
    mock_open().read.return_value = current_test

    # execute without file update
    actual = update_test_of_factory(
        component,
        module_name,
        class_name,
        class_alias,
        config_model_name,
        with_file_update=False,
    )
    # assert
    assert actual == expected_test
    mock_open.assert_called_with(
        os.path.join(
            COMPONENT_SUBPACKAGE_DIR_MAP[component].replace(PACKAGE_DIR, './tests'),  # noqa
            'test_factory.py',
        ),
        'r',
        encoding='utf-8',
    )
    mock_open().write.assert_not_called()

    # execute with file update
    actual = update_test_of_factory(
        component,
        module_name,
        class_name,
        class_alias,
        config_model_name,
        with_file_update=True,
    )
    # assert
    assert actual == expected_test
    mock_open().write.assert_called_once_with(expected_test)
