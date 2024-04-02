from __future__ import annotations
import datetime
from pydantic import BaseModel
from .typing_target_model import TypingTargetModel
from .record_model import RecordModel


class OutputModel(BaseModel):

    timestamp: datetime.datetime
    typing_target: TypingTargetModel
    records: list[RecordModel]
