from fastapi import APIRouter, Depends
from app.db import get_db
from app.services.bird_instantaneous_velocity import generate_problem, submit_attempt
from app.schemas.bird_instantaneous_velocity import (
    BirdInstantaneousVelocityProblemResponse,
    BirdInstantaneousVelocityAttemptRequest,
    BirdInstantaneousVelocityAttemptResponse
)

router = APIRouter()


@router.get("/generate-problem")
def generate_bird_instantaneous_velocity_problem(db=Depends(get_db)) -> BirdInstantaneousVelocityProblemResponse:
    bird_instantaneous_velocity_problem = generate_problem(
        db=db
    )

    return bird_instantaneous_velocity_problem


@router.post("/submit-attempt")
def submit_bird_instantaneous_velocity_attempt(
    request: BirdInstantaneousVelocityAttemptRequest,
    db=Depends(get_db)
) -> BirdInstantaneousVelocityAttemptResponse:
    bird_instantaneous_velocity_attempt = submit_attempt(
        request=request,
        db=db
    )

    return bird_instantaneous_velocity_attempt