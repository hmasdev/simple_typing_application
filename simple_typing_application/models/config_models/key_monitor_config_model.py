from pydantic import BaseModel


class BaseKeyMonitorConfigModel(BaseModel):
    pass


class PynputBasedKeyMonitorConfigModel(BaseKeyMonitorConfigModel):
    pass


class SSHKeyboardBasedKeyMonitorConfigModel(BaseKeyMonitorConfigModel):
    pass
