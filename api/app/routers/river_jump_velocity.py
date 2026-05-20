from fastapi import APIRouter, Depends
from app.db import get_db
from app.services.river_jump_velocity import (
    generate_problem,
    submit_attempt_a,
    submit_attempt_b,
)
from app.schemas.river_jump_velocity import (
    RiverJumpVelocityProblemResponse,
    RiverJumpVelocityPartAAttemptRequest,
    RiverJumpVelocityPartAAttemptResponse,
    RiverJumpVelocityPartBAttemptRequest,
    RiverJumpVelocityPartBAttemptResponse,
)

router = APIRouter()


@router.get("/generate-problem")
def generate_river_jump_velocity_problem(
    db=Depends(get_db)
) -> RiverJumpVelocityProblemResponse:
    river_jump_velocity_problem = generate_problem(
        db=db
    )

    return river_jump_velocity_problem


@router.post("/submit-attempt-a")
def submit_river_jump_velocity_attempt_a(
    request: RiverJumpVelocityPartAAttemptRequest,
    db=Depends(get_db)
) -> RiverJumpVelocityPartAAttemptResponse:
    river_jump_velocity_attempt_a = submit_attempt_a(
        request=request,
        db=db
    )

    return river_jump_velocity_attempt_a


@router.post("/submit-attempt-b")
def submit_river_jump_velocity_attempt_b(
    request: RiverJumpVelocityPartBAttemptRequest,
    db=Depends(get_db)
) -> RiverJumpVelocityPartBAttemptResponse:
    river_jump_velocity_attempt_b = submit_attempt_b(
        request=request,
        db=db
    )

    return river_jump_velocity_attempt_b