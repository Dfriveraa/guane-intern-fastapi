from app.db.models import Dog, User
from app.crud.user import find_user_by_id
from app.services.api_images import get_random_image
from app.schemas.dog import DogUpdateIn
from typing import Union, List


async def create_dog(name: str, publisher: User):
    image = await get_random_image()
    new_dog = Dog(name=name, picture=image, publisher=publisher, adopter=None)
    await new_dog.save()
    return new_dog


async def find_dog_by_name(name: str) -> Union[Dog, None]:
    dog = await Dog.filter(name=name).prefetch_related("publisher", "adopter").first()
    if dog:
        return dog
    return None


async def get_dogs(offset: int, limit: int, adopted: bool = None) -> List[Dog]:
    if adopted is None:
        dogs = await Dog.all().prefetch_related("publisher", "adopter").offset(offset).limit(limit)
    else:
        dogs = await Dog.filter(is_adopted=adopted).all().prefetch_related("publisher", "adopter").offset(offset).limit(
            limit)
    return dogs


async def remove_adopter(dog: Dog):
    dog.is_adopted = False
    dog.adopter = None
    await dog.save()
    return Dog


async def add_adopter(adopter: User, dog: Dog):
    if not dog.is_adopted:
        dog.is_adopted = True
        dog.adopter_id = adopter.id
        await dog.save()
    return dog


async def delete_dog(dog: Dog, user: User):
    if user.id == dog.publisher.id or user.id == dog.adopter.id:
        await dog.delete()
        return True
    else:
        return False
