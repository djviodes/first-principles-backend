import uuid

from datetime import datetime
from pydantic import BaseModel, ConfigDict

class DropTimeProblemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    height: float
    walker_start: float
    walker_velocity: float

class DropTimeAttemptRequest(BaseModel):
    problem_id: uuid.UUID
    student_drop_time: float

class DropTimeAttemptResponse(BaseModel):
    id: uuid.UUID
    created_at: datetime
    target_hit: bool
    correct_drop_time: float
    balloon_positions: list[float]
    walker_positions: list[float]
