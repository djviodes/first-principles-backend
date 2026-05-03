import random

from math_and_physics import compute_straight_line_acceleration
from app.core.errors import SimulationError
from app.models.straight_line_acceleration import (
    StraightLineAccelerationProblem,
    StraightLineAccelerationAttempt,
)
from app.schemas.straight_line_acceleration import (
    StraightLineAccelerationProblemResponse,
    StraightLineAccelerationAttemptRequest,
    StraightLineAccelerationAttemptResponse,
)

from sqlalchemy.orm import Session


def generate_problem(db: Session) -> StraightLineAccelerationProblem:
    distance = random.uniform(50.0, 100.0)
    time = random.uniform(5.0, 6.0)

    straight_line_acceleration_problem_obj = StraightLineAccelerationProblem(
        distance=distance,
        time=time
    )

    db.add(straight_line_acceleration_problem_obj)
    db.commit()
    db.refresh(straight_line_acceleration_problem_obj)

    return StraightLineAccelerationProblemResponse.model_validate(
        straight_line_acceleration_problem_obj
    )


def submit_attempt(
    request: StraightLineAccelerationAttemptRequest,
    db: Session
) -> StraightLineAccelerationAttemptResponse:
    problem_data = db.get(StraightLineAccelerationProblem, request.problem_id)

    if problem_data is None:
        raise SimulationError(
            message="Problem not found",
            status_code=404
        )
    
    straight_line_acceleration_results = compute_straight_line_acceleration(
        request.student_straight_line_acceleration,
        problem_data.distance,
        problem_data.time
    )

    straight_line_acceleration_attempt_obj = StraightLineAccelerationAttempt(
        problem_id=request.problem_id,
        student_straight_line_acceleration=request.student_straight_line_acceleration,
        correct_straight_line_acceleration=straight_line_acceleration_results.correct_straight_line_acceleration,
        time_hit=straight_line_acceleration_results.hit
    )

    db.add(straight_line_acceleration_attempt_obj)
    db.commit()
    db.refresh(straight_line_acceleration_attempt_obj)

    return StraightLineAccelerationAttemptResponse(
        id=straight_line_acceleration_attempt_obj.id,
        created_at=straight_line_acceleration_attempt_obj.created_at,
        time_hit=straight_line_acceleration_results.hit,
        correct_straight_line_acceleration=straight_line_acceleration_results.correct_straight_line_acceleration,
        car_positions=straight_line_acceleration_results.car_positions
    )