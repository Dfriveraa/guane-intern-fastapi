from fastapi import APIRouter, Depends, HTTPException, Response
from app.db.models import User
from app.schemas.dog import DogBase, ListDogs, DogUpdateIn
from app.crud.dog import create_dog, find_dog_by_name, get_dogs, delete_dog, add_adopter, remove_adopter
from app.crud.user import find_user_by_id
from app.core.security.auth import get_current_active_user
from typing import Optional

router = APIRouter()


@router.get("/", response_model=ListDogs)
async def get_all_dogs(adopted: Optional[bool] = None, offset: int = 0, limit: int = 10):
    dogs = await get_dogs(offset=offset, adopted=adopted, limit=limit)
    list_dogs = ListDogs(offset=offset, limit=limit, total=len(dogs), dogs=dogs)
    return list_dogs


@router.put("/{name}", response_model=DogBase)
async def remove_dog_adopter(name: str, user: User = Depends(get_current_active_user)):
    dog = await handler(name, user)
    dog_updated = await remove_adopter(dog)
    return dog_updated


@router.put("/adopt/{name}",response_model=DogBase)
async def adopt_dog(name: str, dog_update: DogUpdateIn, user: User = Depends(get_current_active_user)):
    dog = await handler(name, user)
    adopter = await handler_adoption(dog_update.adopter_id)
    dog_updated = await add_adopter(adopter=adopter, dog=dog)
    if not dog_updated:
        raise HTTPException(status_code=403, detail="This changes was not allowed")
    else:
        return dog_updated


@router.post("/{name}", response_model=DogBase)
async def register_new_dog(name: str, publisher: User = Depends(get_current_active_user)):
    if await find_dog_by_name(name=name):
        raise HTTPException(status_code=409, detail="There is already a dog with this name")
    dog = await create_dog(name=name, publisher=publisher)
    return dog


@router.get("/{name}", response_model=DogBase)
async def get_dog_info(name: str):
    dog = await find_dog_by_name(name=name)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog with this name not found")
    else:
        return dog


@router.delete("/{name}")
async def delete_dog_register(name: str, user: User = Depends(get_current_active_user)):
    dog = await find_dog_by_name(name=name)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog with this name not found")
    status = await delete_dog(dog=dog, user=user)
    if status:
        return Response(status_code=204)
    else:
        return Response(status_code=500)


async def handler(name: str, user: User):
    dog = await find_dog_by_name(name=name)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    if not (user.id == (dog.publisher.id or dog.adopter.id)):
        raise HTTPException(status_code=401, detail="Unauthorized user to this")
    return dog


async def handler_adoption(user_id: int):
    user = await find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User with this id not found")
    return user
