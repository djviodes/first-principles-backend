import random

from app.core.errors import SimulationError
from math_and_physics import (
    river_jump_velocity_part_a,
    river_jump_velocity_part_b,
)
from app.models.river_jump_velocity import (
    RiverJumpVelocityProblem,
    RiverJumpVelocityPartAAttempt,
    RiverJumpVelocityPartBAttempt,
)
from app.schemas.river_jump_velocity import (
    RiverJumpVelocityProblemResponse,
    RiverJumpVelocityPartAAttemptRequest,
    RiverJumpVelocityPartAAttemptResponse,
    RiverJumpVelocityPartBAttemptRequest,
    RiverJumpVelocityPartBAttemptResponse,
)

from sqlalchemy.orm import Session


def generate_problem(db: Session) -> RiverJumpVelocityProblem:
    x_f = random.uniform(43.0, 53.0)
    y_i = random.uniform(16.3, 26.3)
    y_f = random.uniform(1.0, 4.5)

    river_jump_velocity_problem_obj = RiverJumpVelocityProblem(
        x_f=x_f,
        y_i=y_i,
        y_f=y_f,
    )

    db.add(river_jump_velocity_problem_obj)
    db.commit()
    db.refresh(river_jump_velocity_problem_obj)

    return RiverJumpVelocityProblemResponse.model_validate(
        river_jump_velocity_problem_obj
    )


def submit_attempt_a(
    request: RiverJumpVelocityPartAAttemptRequest,
    db: Session
) -> RiverJumpVelocityPartAAttemptResponse:
    problem_data = db.get(RiverJumpVelocityProblem, request.problem_id)

    if problem_data is None:
        raise SimulationError(
            message="Problem not found",
            status_code=404
        )

    river_jump_velocity_part_a_results = river_jump_velocity_part_a(
        request.student_x_velocity,
        x_f=problem_data.x_f,
        y_i=problem_data.y_i,
        y_f=problem_data.y_f,
    )

    river_jump_velocity_attempt_a_obj = RiverJumpVelocityPartAAttempt(
        problem_id=request.problem_id,
        student_x_velocity=request.student_x_velocity,
        velocity_hit=river_jump_velocity_part_a_results.hit,
        correct_x_velocity=river_jump_velocity_part_a_results.correct_x_velocity,
    )

    db.add(river_jump_velocity_attempt_a_obj)
    db.commit()
    db.refresh(river_jump_velocity_attempt_a_obj)

    return RiverJumpVelocityPartAAttemptResponse(
        id=river_jump_velocity_attempt_a_obj.id,
        created_at=river_jump_velocity_attempt_a_obj.created_at,
        velocity_hit=river_jump_velocity_part_a_results.hit,
        correct_x_velocity=river_jump_velocity_part_a_results.correct_x_velocity,
        car_x_positions=river_jump_velocity_part_a_results.car_x_positions,
        car_y_positions=river_jump_velocity_part_a_results.car_y_positions,
    )


def submit_attempt_b(
    request: RiverJumpVelocityPartBAttemptRequest,
    db: Session
) -> RiverJumpVelocityPartBAttemptResponse:
    problem_data = db.get(RiverJumpVelocityProblem, request.problem_id)

    if problem_data is None:
        raise SimulationError(
            message="Problem not found",
            status_code=404
        )

    river_jump_velocity_part_b_results = river_jump_velocity_part_b(
        request.student_final_velocity,
        x_f=problem_data.x_f,
        y_i=problem_data.y_i,
        y_f=problem_data.y_f,
    )

    river_jump_velocity_attempt_b_obj = RiverJumpVelocityPartBAttempt(
        problem_id=request.problem_id,
        student_final_velocity=request.student_final_velocity,
        final_velocity_hit=river_jump_velocity_part_b_results.hit,
        correct_final_velocity=river_jump_velocity_part_b_results.correct_final_velocity,
    )

    db.add(river_jump_velocity_attempt_b_obj)
    db.commit()
    db.refresh(river_jump_velocity_attempt_b_obj)

    return RiverJumpVelocityPartBAttemptResponse(
        id=river_jump_velocity_attempt_b_obj.id,
        created_at=river_jump_velocity_attempt_b_obj.created_at,
        final_velocity_hit=river_jump_velocity_part_b_results.hit,
        correct_final_velocity=river_jump_velocity_part_b_results.correct_final_velocity,
    )