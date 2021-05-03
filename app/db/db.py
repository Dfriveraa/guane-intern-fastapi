from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from app.core.config import get_settings

settings = get_settings()


def init_db(app: FastAPI):
    register_tortoise(
        app,
        db_url=settings.database_url,
        modules={"models": ['app.db.models']},
        generate_schemas=False,
        add_exception_handlers=True
    )


async def generate_schema():
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ['app.db.models']}
    )

    await Tortoise.generate_schemas()
    await Tortoise.close_connections()
