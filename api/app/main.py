from fastapi import FastAPI
from app.routers.freefall import router as freefall_router
from app.core.errors import register_error_handlers
from app.core.logging import logger

app = FastAPI()
register_error_handlers(app=app)


app.include_router(freefall_router, prefix="/api/v1", tags=["Freefall"])