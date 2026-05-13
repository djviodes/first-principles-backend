import uuid

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SquirrelPositionAndVelocityProblemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    a_x: float
    b_x: float
    c_y: float
    time: float


class SquirrelPositionAndVelocityAttemptARequest(BaseModel):
    problem_id: uuid.UUID
    student_a_x: float
    student_b_x: float
    student_c_y: float


class SquirrelPositionAndVelocityAttemptAResponse(BaseModel):
    id: uuid.UUID
    created_at: datetime
    coefficient_hit: bool
    correct_a_x: float
    correct_b_x: float
    correct_c_y: float
    squirrel_x_positions: list[float]
    squirrel_y_positions: list[float]


class SquirrelPositionAndVelocityAttemptBRequest(BaseModel):
    problem_id: uuid.UUID
    student_distance: float


class SquirrelPositionAndVelocityAttemptBResponse(BaseModel):
    id: uuid.UUID
    created_at: datetime
    distance_hit: bool
    correct_distance: float


class SquirrelPositionAndVelocityAttemptCRequest(BaseModel):
    problem_id: uuid.UUID
    student_magnitude: float
    student_direction: float


class SquirrelPositionAndVelocityAttemptCResponse(BaseModel):
    id: uuid.UUID
    created_at: datetime
    magnitude_and_direction_hit: bool
    correct_magnitude: float
    correct_direction: float