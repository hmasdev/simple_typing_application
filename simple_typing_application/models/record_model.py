import datetime
from pydantic import BaseModel, Field


class RecordModel(BaseModel):

    timestamp: datetime.datetime = Field(..., description="The timestamp when the key was pressed.")  # noqa
    pressed_key: str = Field(..., description="The pressed key.")
    correct_keys: list[str] = Field([], description="The correct keys.")
    is_correct: bool = Field(False, description="Whether the pressed key is correct or not.")  # noqa
