import random

from math_and_physics import compute_drop_time
from app.models.drop_time import DropTimeProblem, DropTimeAttempt
from app.schemas.drop_time import DropTimeProblemResponse, DropTimeAttemptRequest, DropTimeAttemptResponse
from app.core.errors import SimulationError

from sqlalchemy.orm import Session


def generate_problem(db: Session) -> DropTimeProblem:
    height = random.uniform(20.0, 80.0)
    walker_start = random.uniform(15.0, 40.0)
    walker_velocity = random.uniform(-1.0, -3.0)

    drop_time_problem_obj = DropTimeProblem(
        height=height,
        walker_start=walker_start,
        walker_velocity=walker_velocity
    )

    db.add(drop_time_problem_obj)
    db.commit()
    db.refresh(drop_time_problem_obj)

    return DropTimeProblemResponse.model_validate(drop_time_problem_obj)


def submit_attempt(request: DropTimeAttemptRequest, db: Session) -> DropTimeAttemptResponse:
    problem_data = db.get(DropTimeProblem, request.problem_id)

    if problem_data is None:
        raise SimulationError(
            message="Problem not found",
            status_code=404
        )

    drop_time_results = compute_drop_time(
        request.student_drop_time,
        problem_data.height,
        problem_data.walker_start,
        problem_data.walker_velocity
    )

    drop_time_attempt_obj = DropTimeAttempt(
        problem_id=request.problem_id,
        student_drop_time=request.student_drop_time,
        correct_drop_time=drop_time_results.correct_drop_time,
        target_hit=drop_time_results.hit,
    )

    db.add(drop_time_attempt_obj)
    db.commit()
    db.refresh(drop_time_attempt_obj)

    return DropTimeAttemptResponse(
        id=drop_time_attempt_obj.id,
        created_at=drop_time_attempt_obj.created_at,
        target_hit=drop_time_results.hit,
        correct_drop_time=drop_time_results.correct_drop_time,
        balloon_positions=drop_time_results.balloon_positions,
        walker_positions=drop_time_results.walker_positions
    )
