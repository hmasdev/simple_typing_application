from pydantic import BaseModel
from .typing_target_model import TypingTargetModel
from .record_model import RecordModel


class OutputModel(BaseModel):

    typing_target: TypingTargetModel
    records: list[RecordModel]
