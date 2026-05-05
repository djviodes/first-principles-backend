import uuid

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TrainStopDistanceProblemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    velocity: float
    acceleration: float


class TrainStopDistanceAttemptRequest(BaseModel):
    problem_id: uuid.UUID
    student_train_stop_distance: float


class TrainStopDistanceAttemptResponse(BaseModel):
    id: uuid.UUID
    created_at: datetime
    distance_hit: bool
    correct_train_stop_distance: float
    train_positions: list[float]