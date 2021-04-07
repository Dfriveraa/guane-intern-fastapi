from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserRegister, UserUpdateIn, UserToken, UserBase, UserUpdateOut
from app.schemas.custom import Token
from app.crud.user import create_user, find_user_by_email, update_user, update_user_active
from app.db.db import get_db
from app.core.security.utils import verify_password
from app.core.security.auth import create_access_token, get_current_active_user
from app.db.models import User

router = APIRouter()


@router.put("/", response_model=UserUpdateOut)
def update_user_info(user_updated: UserUpdateIn, user: User = Depends(get_current_active_user),
                           db: Session = Depends(get_db)):
    user = update_user(db=db, user=user, user_update=user_updated)
    return user


@router.put("/state")
def update_user_info(user: User = Depends(get_current_active_user),
                           db: Session = Depends(get_db)):
    user = update_user_active(db=db, user=user, new_state=False)
    return user


@router.get("/info", response_model=UserBase)
async def get_personal_info(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = find_user_by_email(db=db, email=form_data.username.lower())
    if not user or not verify_password(plain_password=form_data.password, hashed_password=user.password_hashed):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    else:
        token = UserToken(id=user.id, email=user.email)
        access_token = create_access_token(token)
        return Token(access_token=access_token)


@router.post("/", response_model=UserBase)
def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    if find_user_by_email(db, user_in.email.lower()):
        raise HTTPException(status_code=409, detail="There is already a user with this email")

    user = create_user(db=db, user_register=user_in)
    return user
