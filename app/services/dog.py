from typing import TypeVar, Optional, Dict, Any

from app.infra.postgres.crud.dog import CrudDog, crud_dog
from app.schemas.dog import DogCreate, DogUpdateIn
from app.services.api_images import get_random_image

QueryType = TypeVar("QueryType", bound=CrudDog)


class ServiceDog:
    def __init__(self, query: QueryType):
        self.__query = query

    async def create_dog(self, *, name: str, publisher_id: int):
        picture = await get_random_image()
        dog_in = DogCreate(name=name, picture=picture, publisher_id=publisher_id)
        dog = await self.__query.create(obj_in=dog_in)
        return dog

    async def find_dog_by_name(self, *, name: str) -> Optional[Dict[str, Any]]:
        dog = await self.__query.get_by_unique_field(name=name)
        if dog:
            return dog
        return None

    async def get_all_dogs(self, *, offset: int, limit: int, adopted: bool = None):
        dogs = await self.__query.get_dogs(offset=offset, limit=limit, adopted=adopted)
        return dogs

    async def change_adopter(self, *, _id: int, adopter_id: Optional[int]):
        if adopter_id:
            update_dog = DogUpdateIn(adopter_id=adopter_id, is_adopted=True)
            dog = await self.__query.update(_id=_id, obj_in=update_dog)
        else:
            update_dog = DogUpdateIn(is_adopted=False)
            dog = await self.__query.other_update(_id=_id, update=update_dog)
        return dog

    async def delete_dog(self, *, _id: int):
        identify = await self.__query.delete(_id=_id)
        if identify == 1:
            return True
        return False


dog_service = ServiceDog(query=crud_dog)
