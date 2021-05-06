from typing import Dict, Any, List, Union, Optional, Generic

from app.schemas.general import CreateSchemaType, UpdateSchemaType, ModelType


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model):
        self._model = model

    async def get_all(self, *, payload: Dict[str, Any], offset: int = 0, limit: int = 15) -> List[Dict[str, Any]]:
        if payload:
            models = await self._model.all().filter(**payload).offset(offset).limit(limit).values()
        else:
            models = await self._model.all().offset(offset).limit(limit).values()
        return models

    async def create(self, *, obj_in: CreateSchemaType) -> Union[dict, None]:
        model_fields = obj_in.dict()
        model = self._model(**model_fields)
        await model.save()
        return model

    async def update(self, *, _id: int, obj_in: UpdateSchemaType) -> Optional[Dict[str, Any]]:
        model = await self._model.filter(id=_id).update(**obj_in.dict(exclude_unset=True))
        if model:
            update_model = await self._model.filter(id=_id).first().values()
            model_m = self._model(**update_model[0])
            update_fields = list(update_model[0].keys())
            await model_m.save(update_fields=update_fields)
            return update_model[0]
        return None

    async def delete(self, *, _id: int) -> int:
        model = await self._model.filter(id=_id).first().delete()
        return model

    async def get_by_id(self, *, _id: int) -> Optional[Dict[str, Any]]:
        if _id:
            model = await self._model.filter(id=_id).first()
            if model:
                return model
            return None
        else:
            return None

    async def get_by_unique_field(self, **kwargs: Union[str, int]) -> Optional[Dict[str, Any]]:
        model = await self._model.filter(**kwargs).first()
        if model:
            return model
        return None
