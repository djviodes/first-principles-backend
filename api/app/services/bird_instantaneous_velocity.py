import random

from math_and_physics import compute_bird_instantaneous_velocity
from app.core.errors import SimulationError
from app.models.bird_instantaneous_velocity import (
    BirdInstantaneousVelocityProblem,
    BirdInstantaneousVelocityAttempt,
)
from app.schemas.bird_instantaneous_velocity import (
    BirdInstantaneousVelocityProblemResponse,
    BirdInstantaneousVelocityAttemptRequest,
    BirdInstantaneousVelocityAttemptResponse,
)

from sqlalchemy.orm import Session


def generate_problem(db: Session) -> BirdInstantaneousVelocityProblem:
    function_types = ["linear", "quadratic", "cubic"]
    function_type = random.choice(function_types)

    match function_type:
        case "linear":
            a = random.uniform(4.0, 14.0)
            b = random.uniform(1.0, 10.0)
            c = None
            d = None
        case "quadratic":
            a = random.uniform(0.1, 1.0)
            b = random.uniform(1.0, 5.0)
            c = random.uniform(1.0, 10.0)
            d = None
        case "cubic":
            a = random.uniform(0.001, 0.01)
            b = random.uniform(0.5, 1.0)
            c = random.uniform(1.0, 7.0)
            d = random.uniform(1.0, 10.0)
        case _:
            raise ValueError("Invalid function type")

    time = random.uniform(1.0, 10.0)

    bird_instantaneous_velocity_problem_obj = BirdInstantaneousVelocityProblem(
        function_type=function_type,
        a=a,
        b=b,
        c=c,
        d=d,
        time=time,
    )

    db.add(bird_instantaneous_velocity_problem_obj)
    db.commit()
    db.refresh(bird_instantaneous_velocity_problem_obj)

    return BirdInstantaneousVelocityProblemResponse.model_validate(
        bird_instantaneous_velocity_problem_obj
    )


def submit_attempt(
    request: BirdInstantaneousVelocityAttemptRequest,
    db: Session
) -> BirdInstantaneousVelocityAttemptResponse:
    problem_data = db.get(BirdInstantaneousVelocityProblem, request.problem_id)

    if problem_data is None:
        raise SimulationError(
            message="Problem not found",
            status_code=404
        )
    
    bird_instantaneous_velocity_results = compute_bird_instantaneous_velocity(
        request.student_bird_instantaneous_velocity,
        problem_data.function_type,
        problem_data.time,
        problem_data.a,
        problem_data.b,
        problem_data.c,
        problem_data.d
    )

    bird_instantaneous_velocity_attempt_obj = BirdInstantaneousVelocityAttempt(
        problem_id=request.problem_id,
        student_bird_instantaneous_velocity=request.student_bird_instantaneous_velocity,
        correct_bird_instantaneous_velocity=bird_instantaneous_velocity_results.correct_instantaneous_velocity,
        velocity_hit=bird_instantaneous_velocity_results.hit
    )

    db.add(bird_instantaneous_velocity_attempt_obj)
    db.commit()
    db.refresh(bird_instantaneous_velocity_attempt_obj)

    return BirdInstantaneousVelocityAttemptResponse(
        id=bird_instantaneous_velocity_attempt_obj.id,
        created_at=bird_instantaneous_velocity_attempt_obj.created_at,
        velocity_hit=bird_instantaneous_velocity_results.hit,
        correct_bird_instantaneous_velocity=bird_instantaneous_velocity_results.correct_instantaneous_velocity,
        bird_positions=bird_instantaneous_velocity_results.bird_positions
    )