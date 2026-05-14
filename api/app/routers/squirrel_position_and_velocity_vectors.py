from fastapi import APIRouter, Depends
from app.db import get_db
from app.services.squirrel_position_and_velocity_vectors import (
    generate_problem,
    submit_attempt_a,
    submit_attempt_b,
    submit_attempt_c
)
from app.schemas.squirrel_position_and_velocity_vectors import (
    SquirrelPositionAndVelocityProblemResponse,
    SquirrelPositionAndVelocityAttemptARequest,
    SquirrelPositionAndVelocityAttemptAResponse,
    SquirrelPositionAndVelocityAttemptBRequest,
    SquirrelPositionAndVelocityAttemptBResponse,
    SquirrelPositionAndVelocityAttemptCRequest,
    SquirrelPositionAndVelocityAttemptCResponse
)

router = APIRouter()


@router.get("/generate-problem")
def generate_squirrel_position_and_velocity_problem(
    db=Depends(get_db)
) -> SquirrelPositionAndVelocityProblemResponse:
    squirrel_position_and_velocity_problem = generate_problem(
        db=db
    )

    return squirrel_position_and_velocity_problem


@router.post("/submit-attempt-a")
def submit_squirrel_position_and_velocity_attempt_a(
    request: SquirrelPositionAndVelocityAttemptARequest,
    db=Depends(get_db)
) -> SquirrelPositionAndVelocityAttemptAResponse:
    squirrel_position_and_velocity_attempt_a = submit_attempt_a(
        request=request,
        db=db
    )

    return squirrel_position_and_velocity_attempt_a


@router.post("/submit-attempt-b")
def submit_squirrel_position_and_velocity_attempt_b(
    request: SquirrelPositionAndVelocityAttemptBRequest,
    db=Depends(get_db)
) -> SquirrelPositionAndVelocityAttemptBResponse:
    squirrel_position_and_velocity_attempt_b = submit_attempt_b(
        request=request,
        db=db
    )

    return squirrel_position_and_velocity_attempt_b


@router.post("/submit-attempt-c")
def submit_squirrel_position_and_velocity_attempt_c(
    request: SquirrelPositionAndVelocityAttemptCRequest,
    db=Depends(get_db)
) -> SquirrelPositionAndVelocityAttemptCResponse:
    squirrel_position_and_velocity_attempt_c = submit_attempt_c(
        request=request,
        db=db
    )

    return squirrel_position_and_velocity_attempt_c