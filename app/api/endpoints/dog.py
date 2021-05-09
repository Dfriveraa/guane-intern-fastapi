from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response

from app.core.celery import celery_app
from app.core.security.auth import get_current_active_user
from app.infra.postgres.models import User
from app.schemas.dog import ListDogs, DogBase, DogInfo
from app.services.dog import dog_service
from app.services.user import user_service
import asyncio
router = APIRouter()


@router.get("/", response_model=ListDogs)
def get_all_dogs(adopted: Optional[bool] = None, offset: int = 0, limit: int = 10):
    dogs = asyncio.run(dog_service.get_all_dogs(offset=offset, adopted=adopted, limit=limit))
    list_dogs = ListDogs(offset=offset, limit=limit, total=len(dogs), dogs=dogs)
    return list_dogs


@router.put("/{name}", response_model=DogBase)
async def remove_dog_adopter(name: str, user: User = Depends(get_current_active_user)):
    dog = await handler(name, user)
    dog_updated = await dog_service.change_adopter(_id=dog.id, adopter_id=None)
    return dog_updated


@router.put("/adopt/{name}", response_model=DogBase)
async def adopt_dog(name: str, adopter_id: int, user: User = Depends(get_current_active_user)):
    dog = await handler(name, user)
    adopter = await handler_adoption(adopter_id)
    dog_updated = await dog_service.change_adopter(_id=dog.id, adopter_id=adopter.id)
    if not dog_updated:
        raise HTTPException(status_code=403, detail="This changes was not allowed")
    else:
        return dog_updated


@router.post("/{name}")
async def register_new_dog(name: str, publisher: User = Depends(get_current_active_user)):
    if await dog_service.find_dog_by_name(name=name):
        raise HTTPException(status_code=409, detail="There is already a dog with this name")
    celery_app.send_task("app.workers.dogs.create_dog_worker", args=[name,publisher.id])

    # dog = await dog_service.create_dog(name=name, publisher_id=publisher.id)
    return {"Message": "Creating dog"}


@router.get("/{name}", response_model=DogInfo)
async def get_dog_info(name: str):
    dog = await dog_service.find_dog_by_name(name=name)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog with this name not found")
    else:
        return dog


@router.delete("/{name}")
async def delete_dog_register(name: str, user: User = Depends(get_current_active_user)):
    dog = await dog_service.find_dog_by_name(name=name)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog with this name not found")
    if user.id == (dog.publisher_id or dog.adopter_id):
        status = await dog_service.delete_dog(_id=dog.id)
        if status:
            return Response(status_code=204)
        else:
            return Response(status_code=500)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized user to this")


async def handler(name: str, user: User):
    dog = await dog_service.find_dog_by_name(name=name)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    if not (user.id == (dog.publisher_id or dog.adopter_id)):
        raise HTTPException(status_code=401, detail="Unauthorized user to this")
    return dog


async def handler_adoption(user_id: int):
    user = await user_service.find_user_by_id(_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User with this id not found")
    return user
