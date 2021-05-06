from typing import TypeVar, Optional, Dict, Any

from app.core.security.utils import get_password_hash
from app.infra.postgres.crud.user import CrudUser, crud_user
from app.infra.postgres.models import User
from app.schemas.user import UserRegister, UserUpdateIn

QueryType = TypeVar("QueryType", bound=CrudUser)


class ServiceUser:
    def __init__(self, query: QueryType):
        self.__query = query

    async def create_user(self, *, user_register: UserRegister):
        user_register.email = user_register.email.lower()
        user_register.password = get_password_hash(user_register.password)
        user = await self.__query.create(obj_in=user_register)
        return user

    async def find_user_by_email(self, *, email: str) -> Optional[User]:
        user = await self.__query.get_by_unique_field(email=email)
        if user:
            return user
        return None

    async def find_user_by_id(self, *, _id: int) -> Optional[User]:
        user = await self.__query.get_by_id(_id=_id)
        if user:
            return user
        return None

    async def update_user(self, *, _id: int, update: UserUpdateIn) -> Optional[Dict[str, Any]]:
        if update.email:
            update.email = update.email.lower()
        user = await self.__query.update(_id=_id, obj_in=update)
        return user

    async def update_state(self, *, _id: int):
        user = await self.__query.inactive(_id=_id)
        return user


user_service = ServiceUser(query=crud_user)
