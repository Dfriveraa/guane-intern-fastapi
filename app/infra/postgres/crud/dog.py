from typing import List
from app.infra.postgres.crud.base import CrudBase
from app.infra.postgres.models import Dog, User
from app.schemas.dog import DogCreate, DogUpdateIn


class CrudDog(CrudBase[Dog, DogCreate, DogUpdateIn]):

    async def get_dogs(self, offset: int, limit: int, adopted: bool = None) -> List[Dog]:
        if adopted is None:
            dogs = await self._model.all().prefetch_related("publisher", "adopter").offset(offset).limit(limit)
        else:
            dogs = await self._model.filter(is_adopted=adopted).all().prefetch_related("publisher", "adopter").offset(
                offset).limit(
                limit)
        return dogs

    async def other_update(self, _id: int, update: DogUpdateIn):
        dog = await self._model.filter(id=_id).update(**update.dict())
        if dog:
            update_model = await self._model.filter(id=_id).first().values()
            model_m = self._model(**update_model[0])
            update_fields = list(update_model[0].keys())
            await model_m.save(update_fields=update_fields)
            return update_model[0]
        return None


crud_dog = CrudDog(model=Dog)
