import random

from app.core.errors import SimulationError
from math_and_physics import (
    compute_squirrel_part_a,
    compute_squirrel_part_b,
    compute_squirrel_part_c,
)
from app.models.squirrel_position_and_velocity_vectors import (
    SquirrelPositionAndVelocityProblem,
    SquirrelPositionAndVelocityPartAAttempt,
    SquirrelPositionAndVelocityPartBAttempt,
    SquirrelPositionAndVelocityPartCAttempt,
)
from app.schemas.squirrel_position_and_velocity_vectors import (
    SquirrelPositionAndVelocityProblemResponse,
    SquirrelPositionAndVelocityAttemptARequest,
    SquirrelPositionAndVelocityAttemptAResponse,
    SquirrelPositionAndVelocityAttemptBRequest,
    SquirrelPositionAndVelocityAttemptBResponse,
    SquirrelPositionAndVelocityAttemptCRequest,
    SquirrelPositionAndVelocityAttemptCResponse,
)

from sqlalchemy.orm import Session


def generate_problem(db: Session) -> SquirrelPositionAndVelocityProblem:
    a_x = random.uniform(0.140, 0.420)
    b_x = random.uniform(0.0180, 0.0540)
    c_y = random.uniform(0.0100, 0.0280)
    time = random.uniform(2.50, 7.50)

    squirrel_position_and_velocity_problem_obj = SquirrelPositionAndVelocityProblem(
        a_x=a_x,
        b_x=b_x,
        c_y=c_y,
        time=time
    )

    db.add(squirrel_position_and_velocity_problem_obj)
    db.commit()
    db.refresh(squirrel_position_and_velocity_problem_obj)

    return SquirrelPositionAndVelocityProblemResponse.model_validate(
        squirrel_position_and_velocity_problem_obj
    )


def submit_attempt_a(
    request: SquirrelPositionAndVelocityAttemptARequest,
    db: Session
) -> SquirrelPositionAndVelocityAttemptAResponse:
    problem_data = db.get(SquirrelPositionAndVelocityProblem, request.problem_id)

    if problem_data is None:
        raise SimulationError(
            message="Problem not found",
            status_code=404
        )
    
    squirrel_position_and_velocity_a_results = compute_squirrel_part_a(
        request.student_a_x,
        request.student_b_x,
        request.student_c_y,
        problem_data.a_x,
        problem_data.b_x,
        problem_data.c_y,
        problem_data.time
    )

    squirrel_position_and_velocity_attempt_a_obj = SquirrelPositionAndVelocityPartAAttempt(
        problem_id=request.problem_id,
        student_a_x=request.student_a_x,
        student_b_x=request.student_b_x,
        student_c_y=request.student_c_y,
        correct_a_x=squirrel_position_and_velocity_a_results.correct_a_x,
        correct_b_x=squirrel_position_and_velocity_a_results.correct_b_x,
        correct_c_y=squirrel_position_and_velocity_a_results.correct_c_y,
        coefficient_hit=squirrel_position_and_velocity_a_results.hit
    )

    db.add(squirrel_position_and_velocity_attempt_a_obj)
    db.commit()
    db.refresh(squirrel_position_and_velocity_attempt_a_obj)

    return SquirrelPositionAndVelocityAttemptAResponse(
        id=squirrel_position_and_velocity_attempt_a_obj.id,
        created_at=squirrel_position_and_velocity_attempt_a_obj.created_at,
        coefficient_hit=squirrel_position_and_velocity_a_results.hit,
        correct_a_x=squirrel_position_and_velocity_a_results.correct_a_x,
        correct_b_x=squirrel_position_and_velocity_a_results.correct_b_x,
        correct_c_y=squirrel_position_and_velocity_a_results.correct_c_y,
        squirrel_x_positions=squirrel_position_and_velocity_a_results.squirrel_x_positions,
        squirrel_y_positions=squirrel_position_and_velocity_a_results.squirrel_y_positions
    )