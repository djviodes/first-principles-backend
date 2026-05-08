import uuid

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class BirdInstantaneousVelocityProblemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    function_type: str
    time: float
    a: float
    b: float
    c: Optional[float]
    d: Optional[float]


class BirdInstantaneousVelocityAttemptRequest(BaseModel):
    problem_id: uuid.UUID
    student_bird_instantaneous_velocity: float


class BirdInstantaneousVelocityAttemptResponse(BaseModel):
    id: uuid.UUID
    created_at: datetime
    velocity_hit: bool
    correct_bird_instantaneous_velocity: float
    bird_positions: list[float]