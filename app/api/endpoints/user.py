from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security.auth import create_access_token, get_current_active_user
from app.core.security.utils import verify_password
from app.infra.postgres.models import User
from app.schemas.custom import Token
from app.schemas.user import UserRegister, UserUpdateIn, UserToken, UserBase, UserUpdateOut
from app.services.user import user_service

router = APIRouter()


@router.get("/info", response_model=UserBase)
async def get_personal_info(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_service.find_user_by_email(email=form_data.username.lower())
    if not user or not verify_password(plain_password=form_data.password, hashed_password=user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    else:
        token = UserToken(id=user.id, email=user.email)
        access_token = create_access_token(token)
        return Token(access_token=access_token)


@router.post("/", response_model=UserBase)
async def register_user(user_in: UserRegister):
    if await user_service.find_user_by_email(email=user_in.email.lower()):
        raise HTTPException(status_code=409, detail="There is already a user with this email")
    user = await user_service.create_user(user_register=user_in)
    return user


@router.put("/", response_model=UserUpdateOut)
async def update_user_info(user_updated: UserUpdateIn, user: User = Depends(get_current_active_user)):
    user = await user_service.update_user(_id=user.id, update=user_updated)
    return user


@router.put("/state", response_model=UserUpdateOut)
async def update_user_info(user: User = Depends(get_current_active_user)):
    user = await user_service.update_state(_id=user.id)
    return user
