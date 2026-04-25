from fastapi import APIRouter, Depends
from app.db import get_db
from app.services.freefall import run_freefall
from app.schemas.freefall import FreeFallRequest, FreeFallResponse

router = APIRouter()


@router.post("/compute-freefall")
def compute_freefall(request_payload: FreeFallRequest, db=Depends(get_db)) -> FreeFallResponse:
    freefall_resopnse = run_freefall(
        request=request_payload,
        db=db
    )
    
    return freefall_resopnse
