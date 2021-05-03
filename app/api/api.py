from fastapi import APIRouter
from app.api.endpoints import user, dog

api_router = APIRouter()
api_router.include_router(user.router, tags=["Users"], prefix="/user")
api_router.include_router(dog.router, tags=["Dogs"], prefix="/dogs")
