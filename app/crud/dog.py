from sqlalchemy.sql import null
from sqlalchemy.orm import Session
from app.db.models import Dog, User
from app.services.api_images import get_random_image
from app.schemas.dog import DogUpdateIn


async def create_dog(name: str, publisher: User, db: Session):
    image = await get_random_image()
    new_dog = Dog(name=name, picture=image, publisher_id=publisher.id)
    db.add(new_dog)
    db.commit()
    db.refresh(new_dog)
    return new_dog


async def find_dog_by_name(name: str, db: Session):
    dog = db.query(Dog).filter(Dog.name == name).first()
    return dog


async def find_dogs_not_adopted(offset: int, limit: int, db: Session):
    dogs = db.query(Dog).filter(Dog.is_adopted == True).slice(offset, limit).all()
    return dogs


async def get_dogs(offset: int, limit: int, db: Session):
    dogs = db.query(Dog).slice(offset, limit).all()
    return dogs


async def update_dog(dog_update: DogUpdateIn, dog: Dog, user: User, db: Session):
    if dog.publisher_id == user.id and not dog.adopter_id and dog_update.is_adopted:
        dog.is_adopted = True
        dog.adopter_id = dog_update.adopter_id
        db.commit()
        return dog
    elif dog.publisher_id == user.id or dog.adopter_id == user.id and not dog_update.is_adopted:
        dog.is_adopted = False
        dog.adopter_id = null()
        return dog
    else:
        return None


async def delete_dog(dog: Dog, user: User, db: Session):
    if user.id == dog.publisher_id or user.id == dog.adopter_id:
        db.delete(dog)
        db.commit()
        return True
    else:
        return False
