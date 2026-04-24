from math_and_physics import compute_freefall
from app.models.freefall import FreeFall
from app.schemas.freefall import FreeFallRequest, FreeFallResponse

from sqlalchemy.orm import Session


def run_freefall(request: FreeFallRequest, db: Session) -> FreeFallResponse:
    freefall_results = compute_freefall(
        request.drag,
        request.initial_velocity
    )

    freefall_obj = FreeFall(
        drag=request.drag,
        initial_height=freefall_results.initial_height,
        initial_velocity=request.initial_velocity,
        final_velocity=freefall_results.final_velocity,
        acceleration=freefall_results.acceleration,
        time_of_flight=freefall_results.time_of_flight
    )

    db.add(freefall_obj)
    db.commit()
    db.refresh(freefall_obj)

    return FreeFallResponse.model_validate(freefall_obj)
