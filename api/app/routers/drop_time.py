from fastapi import APIRouter, Depends
from app.db import get_db
from app.services.drop_time import generate_problem, submit_attempt
from app.schemas.drop_time import DropTimeAttemptRequest, DropTimeAttemptResponse, DropTimeProblemResponse

router = APIRouter()


@router.get("/generate-problem")
def generate_drop_time_problem(db=Depends(get_db)) -> DropTimeProblemResponse:
    drop_time_problem = generate_problem(
        db=db
    )
    
    return drop_time_problem


@router.post("/submit-attempt")
def submit_drop_time_attempt(request: DropTimeAttemptRequest, db=Depends(get_db)) -> DropTimeAttemptResponse:
    drop_time_attempt = submit_attempt(
        request=request,
        db=db
    )

    return drop_time_attempt
