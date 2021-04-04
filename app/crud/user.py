from sqlalchemy.orm import Session
from app.schemas.user import UserRegister, UserUpdateIn
from app.db.models import User
from app.core.security.utils import get_password_hash


async def create_user(db: Session, user_register: UserRegister):
    lower_email = user_register.email.lower()
    hashed_password = get_password_hash(user_register.password)
    db_user = User(email=lower_email, name=user_register.name, password_hashed=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def find_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


async def update_user(db: Session, user: User, user_update: UserUpdateIn):
    update_dict = user_update.dict(exclude_none=True)
    [setattr(user, key, value) for key, value in update_dict.items()]
    db.commit()
    return user


async def update_user_active(db: Session, user: User, new_state: bool):
    user.active = new_state
    db.commit()
    return user
