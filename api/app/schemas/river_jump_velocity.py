import uuid

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RiverJumpVelocityProblemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    x_f: float
    y_i: float
    y_f: float


class RiverJumpVelocityPartAAttemptRequest(BaseModel):
    problem_id: uuid.UUID
    student_x_velocity: float


class RiverJumpVelocityPartAAttemptResponse(BaseModel):
    id: uuid.UUID
    created_at: datetime
    velocity_hit: bool
    correct_x_velocity: float
    car_x_positions: list[float]
    car_y_positions: list[float]


class RiverJumpVelocityPartBAttemptRequest(BaseModel):
    problem_id: uuid.UUID
    student_final_velocity: float


class RiverJumpVelocityPartBAttemptResponse(BaseModel):
    id: uuid.UUID
    created_at: datetime
    final_velocity_hit: bool
    correct_final_velocity: float