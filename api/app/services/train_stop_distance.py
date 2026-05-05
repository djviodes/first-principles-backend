import random

from math_and_physics import compute_train_stop_distance
from app.core.errors import SimulationError
from app.models.train_stop_distance import (
    TrainStopDistanceProblem,
    TrainStopDistanceAttempt
)
from app.schemas.train_stop_distance import (
    TrainStopDistanceProblemResponse,
    TrainStopDistanceAttemptRequest,
    TrainStopDistanceAttemptResponse
)

from sqlalchemy.orm import Session


def generate_problem(db: Session) -> TrainStopDistanceProblemResponse:
    velocity = random.uniform(11.11, 27.78)
    acceleration = random.uniform(-0.27, -0.09)

    train_stop_distance_problem_obj = TrainStopDistanceProblem(
        velocity=velocity,
        acceleration=acceleration
    )

    db.add(train_stop_distance_problem_obj)
    db.commit()
    db.refresh(train_stop_distance_problem_obj)

    return TrainStopDistanceProblemResponse.model_validate(
        train_stop_distance_problem_obj
    )


def submit_attempt(
    request: TrainStopDistanceAttemptRequest,
    db: Session
) -> TrainStopDistanceAttemptResponse:
    problem_data = db.get(TrainStopDistanceProblem, request.problem_id)

    if problem_data is None:
        raise SimulationError(
            message="Problem not found",
            status_code=404
        )
    
    train_stop_distance_results = compute_train_stop_distance(
        request.student_train_stop_distance,
        problem_data.velocity,
        problem_data.acceleration
    )

    train_stop_distance_attempt_obj = TrainStopDistanceAttempt(
        problem_id=request.problem_id,
        student_train_stop_distance=request.student_train_stop_distance,
        correct_train_stop_distance=train_stop_distance_results.correct_train_stop_distance,
        distance_hit=train_stop_distance_results.hit
    )

    db.add(train_stop_distance_attempt_obj)
    db.commit()
    db.refresh(train_stop_distance_attempt_obj)

    return TrainStopDistanceAttemptResponse(
        id=train_stop_distance_attempt_obj.id,
        created_at=train_stop_distance_attempt_obj.created_at,
        distance_hit=train_stop_distance_results.hit,
        correct_train_stop_distance=train_stop_distance_results.correct_train_stop_distance,
        train_positions=train_stop_distance_results.train_positions
    )