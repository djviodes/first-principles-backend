import random

from math_and_physics import compute_relay_catchup_time
from app.core.errors import SimulationError
from app.models.relay_catchup_time import (
    RelayCatchupTimeProblem,
    RelayCatchupTimeAttempt,
)
from app.schemas.relay_catchup_time import (
    RelayCatchupTimeProblemResponse,
    RelayCatchupTimeAttemptRequest,
    RelayCatchupTimeAttemptResponse,
)

from sqlalchemy.orm import Session


def generate_problem(db: Session) -> RelayCatchupTimeProblem:
    a = random.uniform(1.0, 10.0)
    b_two = random.uniform(1.0, 20.0)
    b_one = random.uniform((b_two + 1.0), 25.0)
    v_two = random.uniform(1.0, 5.0)
    v_one = random.uniform((v_two + 1.0), (v_two + 10.0))
    s_two = random.uniform(15.0, 25.0)
    s_one = random.uniform(0.0, (s_two - 10.0))

    relay_catchup_time_problem_obj = RelayCatchupTimeProblem(
        a=a,
        b_one=b_one,
        b_two=b_two,
        v_one=v_one,
        v_two=v_two,
        s_one=s_one,
        s_two=s_two,
    )

    db.add(relay_catchup_time_problem_obj)
    db.commit()
    db.refresh(relay_catchup_time_problem_obj)

    return RelayCatchupTimeProblemResponse.model_validate(
        relay_catchup_time_problem_obj
    )


def submit_attempt(
    request: RelayCatchupTimeAttemptRequest,
    db: Session
) -> RelayCatchupTimeAttemptResponse:
    problem_data = db.get(RelayCatchupTimeProblem, request.problem_id)

    if problem_data is None:
        raise SimulationError(
            message="Problem not found",
            status_code=404
        )
    
    relay_catchup_time_results = compute_relay_catchup_time(
        request.student_relay_catchup_time,
        problem_data.a,
        problem_data.b_one,
        problem_data.b_two,
        problem_data.v_one,
        problem_data.v_two,
        problem_data.s_one,
        problem_data.s_two
    )

    relay_catchup_time_attempt_obj = RelayCatchupTimeAttempt(
        problem_id=request.problem_id,
        student_relay_catchup_time=request.student_relay_catchup_time,
        correct_relay_catchup_time=relay_catchup_time_results.correct_catchup_time,
        time_hit=relay_catchup_time_results.hit
    )

    db.add(relay_catchup_time_attempt_obj)
    db.commit()
    db.refresh(relay_catchup_time_attempt_obj)

    return RelayCatchupTimeAttemptResponse(
        id=relay_catchup_time_attempt_obj.id,
        created_at=relay_catchup_time_attempt_obj.created_at,
        time_hit=relay_catchup_time_results.hit,
        correct_relay_catchup_time=relay_catchup_time_results.correct_catchup_time,
        runner_one_positions=relay_catchup_time_results.runner_one_positions,
        runner_two_positions=relay_catchup_time_results.runner_two_positions
    )