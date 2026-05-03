from fastapi import APIRouter, Depends
from app.db import get_db
from app.services.straight_line_acceleration import generate_problem, submit_attempt
from app.schemas.straight_line_acceleration import (
    StraightLineAccelerationAttemptRequest,
    StraightLineAccelerationAttemptResponse,
    StraightLineAccelerationProblemResponse,
)

router = APIRouter()


@router.get("/generate-problem")
def generate_straight_line_acceleration_problem(db=Depends(get_db)) -> StraightLineAccelerationProblemResponse:
    straight_line_acceleration_problem = generate_problem(
        db=db
    )

    return straight_line_acceleration_problem


@router.post("/submit-attempt")
def submit_straight_line_acceleration_attempt(
    request: StraightLineAccelerationAttemptRequest,
    db=Depends(get_db)
) -> StraightLineAccelerationAttemptResponse:
    straight_line_acceleration_attempt = submit_attempt(
        request=request,
        db=db
    )

    return straight_line_acceleration_attempt