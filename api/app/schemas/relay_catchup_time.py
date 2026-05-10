import uuid

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RelayCatchupTimeProblemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    a: float
    b_one: float
    b_two: float
    v_one: float
    v_two: float
    s_one: float
    s_two: float


class RelayCatchupTimeAttemptRequest(BaseModel):
    problem_id: uuid.UUID
    student_relay_catchup_time: float


class RelayCatchupTimeAttemptResponse(BaseModel):
    id: uuid.UUID
    created_at: datetime
    time_hit: bool
    correct_relay_catchup_time: float
    runner_one_positions: list[float]
    runner_two_positions: list[float]