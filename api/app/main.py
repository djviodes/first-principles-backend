from fastapi import FastAPI
from app.routers.drop_time import router as drop_time_router
from app.routers.straight_line_acceleration import router as straight_line_acceleration_router
from app.routers.train_stop_distance import router as train_stop_distance_router
from app.routers.bird_instantaneous_velocity import router as bird_instantaneous_velocity_router
from app.core.errors import register_error_handlers
from app.core.logging import logger

app = FastAPI()
register_error_handlers(app=app)


app.include_router(drop_time_router, prefix="/api/v1/drop-time", tags=["Drop_Time"])
app.include_router(
    straight_line_acceleration_router,
    prefix="/api/v1/straight-line-acceleration",
    tags=["Straight_Line_Acceleration"]
)
app.include_router(
    train_stop_distance_router,
    prefix="/api/v1/train-stop-distance",
    tags=["Train_Stop_Distance"]
)
app.include_router(
    bird_instantaneous_velocity_router,
    prefix="/api/v1/bird-instantaneous-velocity",
    tags=["Bird_Instantaneous_Velocity"]
)