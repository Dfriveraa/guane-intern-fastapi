from typing import Optional

from app.infra.postgres.crud.base import CrudBase
from app.infra.postgres.models import User
from app.schemas.user import UserRegister, UserUpdateIn


class CrudUser(CrudBase[User, UserRegister, UserUpdateIn]):

    async def inactive(self, _id: int) -> Optional[User]:
        user = await self._model.filter(id=_id).update(active=False)
        return user


crud_user = CrudUser(User)
