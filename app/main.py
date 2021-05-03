from fastapi import FastAPI
from app.core.config import Settings
from app.api.api import api_router
from app.db.db import init_db, generate_schema

settings = Settings()


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(api_router, prefix="/api")
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    init_db(app)
    await generate_schema()
