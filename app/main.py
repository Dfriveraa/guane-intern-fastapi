from fastapi import FastAPI
from app.core.config import Settings
from app.api.api import api_router

settings = Settings()
app = FastAPI(title=settings.app_name)

app.include_router(api_router, prefix='/api')
