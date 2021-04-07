from datetime import datetime, timedelta
from app.db.db import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user import UserToken
from app.core.config import get_settings
from app.crud.user import find_user_by_email
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/login")
settings = get_settings()


def create_access_token(user: UserToken):
    to_encode = user.dict()
    expire = datetime.utcnow() + timedelta(minutes=20)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_token)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_token)
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = find_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
