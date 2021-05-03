from app.schemas.user import UserRegister, UserUpdateIn
from app.db.models.users import User
from app.core.security.utils import get_password_hash
from typing import Union


async def create_user(user_register: UserRegister):
    lower_email = user_register.email.lower()
    hashed_password = get_password_hash(user_register.password)
    db_user = User(email=lower_email, name=user_register.name, password_hashed=hashed_password)
    await db_user.save()
    return db_user


async def find_user_by_email(email: str) -> Union[User, None]:
    user = await User.filter(email=email).first()
    if user:
        return user
    return None


async def find_user_by_id(id: int) -> Union[User, None]:
    user = await User.filter(id=id).first()
    if user:
        return user
    return None


async def update_user(user: User, user_update: UserUpdateIn):
    update_dict = user_update.dict(exclude_none=True)
    [setattr(user, key, value) for key, value in update_dict.items()]
    await user.save()
    return user


async def update_user_active(user: User, new_state: bool) -> User:
    user.active = new_state
    await user.save()
    return user
