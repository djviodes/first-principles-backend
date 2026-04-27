from fastapi import FastAPI
from app.routers.drop_time import router as drop_time_router
from app.core.errors import register_error_handlers
from app.core.logging import logger

app = FastAPI()
register_error_handlers(app=app)


app.include_router(drop_time_router, prefix="/api/v1/drop-time", tags=["Drop_Time"])