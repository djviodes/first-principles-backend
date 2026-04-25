from fastapi import FastAPI
from app.routers.freefall import router as freefall_router

app = FastAPI()


app.include_router(freefall_router, prefix="/api/v1", tags=["Freefall"])
