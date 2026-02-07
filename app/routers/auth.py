from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import DBUser
from app.schemas import UserOut, UserCreate

from app.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register",response_model = UserOut)
async def register(user_data:UserCreate, db:AsyncSession = Depends(get_db)):
    query = select(DBUser).where(DBUser.email == user_data.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=404, detail="Пользователь с таким email уже существует")

    hashed_password = hash_password(user_data.password)

    new_user = DBUser(
        fio = user_data.fio,
        email = user_data.email,
        password = hashed_password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db:AsyncSession = Depends(get_db)):
    query = select(DBUser).where(DBUser.email == form_data.username)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    if not verify_password(form_data.password,existing_user.password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    access_token =create_access_token(existing_user.id,existing_user.email)

    return {"access_token": access_token, "token_type":"bearer"}