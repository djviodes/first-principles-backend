import uuid

from datetime import datetime
from pydantic import BaseModel, ConfigDict

class StraightLineAccelerationProblemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    distance: float
    time: float


class StraightLineAccelerationAttemptRequest(BaseModel):
    problem_id: uuid.UUID
    student_straight_line_acceleration: float


class StraightLineAccelerationAttemptResponse(BaseModel):
    id: uuid.UUID
    created_at: datetime
    time_hit: bool
    correct_straight_line_acceleration: float
    car_positions: list[float]