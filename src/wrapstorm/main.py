from fastapi import FastAPI
from src.wrapstorm.api.routes import router

app = FastAPI(title="STORM API")

app.include_router(router, prefix="/storm", tags=["STORM"])
