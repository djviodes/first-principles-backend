from fastapi import APIRouter, Depends
from app.db import get_db
from app.services.train_stop_distance import generate_problem, submit_attempt
from app.schemas.train_stop_distance import(
    TrainStopDistanceAttemptRequest,
    TrainStopDistanceAttemptResponse,
    TrainStopDistanceProblemResponse,
)

router = APIRouter()


@router.get("/generate-problem")
def generate_train_stop_distance_problem(db=Depends(get_db)) -> TrainStopDistanceProblemResponse:
    train_stop_distance_problem = generate_problem(
        db=db
    )

    return train_stop_distance_problem


@router.post("/submit-attempt")
def submit_train_stop_distance_attempt(
    request: TrainStopDistanceAttemptRequest,
    db=Depends(get_db)
) -> TrainStopDistanceAttemptResponse:
    train_stop_distance_attempt = submit_attempt(
        request=request,
        db=db
    )

    return train_stop_distance_attempt