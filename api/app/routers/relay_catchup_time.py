from fastapi import APIRouter, Depends
from app.db import get_db
from app.services.relay_catchup_time import generate_problem, submit_attempt
from app.schemas.relay_catchup_time import (
    RelayCatchupTimeProblemResponse,
    RelayCatchupTimeAttemptRequest,
    RelayCatchupTimeAttemptResponse
)

router = APIRouter()


@router.get("/generate-problem")
def generate_relay_catchup_time_problem(db=Depends(get_db)) -> RelayCatchupTimeProblemResponse:
    relay_catchup_time_problem = generate_problem(
        db=db
    )

    return relay_catchup_time_problem


@router.post("/submit-attempt")
def submit_relay_catchup_time_attempt(
    request: RelayCatchupTimeAttemptRequest,
    db=Depends(get_db)
) -> RelayCatchupTimeAttemptResponse:
    relay_catchup_time_attempt = submit_attempt(
        request=request,
        db=db
    )

    return relay_catchup_time_attempt