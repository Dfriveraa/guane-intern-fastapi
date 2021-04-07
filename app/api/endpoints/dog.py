from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.dog import DogBase, ListDogs, DogUpdateIn
from app.crud.dog import create_dog, find_dog_by_name, find_adopted_dogs, get_dogs, update_dog, delete_dog
from app.core.security.auth import get_current_active_user
from app.db.db import get_db

router = APIRouter()


@router.get("/", response_model=ListDogs)
def get_all_dogs(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    dogs = get_dogs(offset=offset, limit=limit, db=db)
    list_dogs = ListDogs(offset=offset, limit=limit, total=len(dogs), dogs=dogs)
    return list_dogs


@router.get("/adopted", response_model=ListDogs)
def get_adopted_dogs(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    dogs = find_adopted_dogs(offset=offset, limit=limit, db=db)
    list_dogs = ListDogs(offset=offset, limit=limit, total=len(dogs), dogs=dogs)
    return list_dogs


@router.put("/{name}", response_model=DogBase)
def change_dog_info(name: str, dog_update: DogUpdateIn, user: User = Depends(get_current_active_user),
                          db: Session = Depends(get_db)):
    dog = find_dog_by_name(name=name, db=db)
    dog_updated = update_dog(dog_update=dog_update, dog=dog, user=user, db=db)
    if not dog_updated:
        raise HTTPException(status_code=403, detail="This changes was not allowed")
    else:
        return dog_updated


@router.post("/{name}", response_model=DogBase)
async def register_new_dog(name: str, publisher: User = Depends(get_current_active_user),
                           db: Session = Depends(get_db)):
    if find_dog_by_name(name=name, db=db):
        raise HTTPException(status_code=409, detail="There is already a dog with this name")

    dog = await create_dog(name=name, publisher=publisher, db=db)
    return dog


@router.get("/{name}", response_model=DogBase)
def get_dog_info(name: str, db: Session = Depends(get_db)):
    dog = find_dog_by_name(name=name, db=db)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog with this name not found")
    else:
        return dog


@router.delete("/{name}")
def delete_dog_register(name: str, user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    dog = find_dog_by_name(name=name, db=db)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog with this name not found")
    status = delete_dog(dog=dog, user=user, db=db)
    if status:
        return Response(status_code=204)
    else:
        return Response(status_code=500)
