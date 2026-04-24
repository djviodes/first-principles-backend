import uuid

from datetime import datetime
from pydantic import BaseModel, ConfigDict

class FreeFallRequest(BaseModel):
    drag: bool
    initial_velocity: float

class FreeFallResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    drag: bool
    initial_height: float
    initial_velocity: float
    final_velocity: float
    acceleration: float
    time_of_flight: float
