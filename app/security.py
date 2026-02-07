from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from dotenv import load_dotenv
import os

from app.database import get_db
from app.models import DBUser

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
AlGORITHM = os.getenv("AlGORITHM")
ACCES_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    return pwd_context.verify(password,hashed_password)


def create_access_token(user_id:int,email:str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": str(user_id),
        "email":email,
        "exp":expire
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=AlGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme),db:AsyncSession = Depends(get_db)):
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[AlGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exeption
    except JWTError:
        raise credentials_exeption

    query = select(DBUser).where(DBUser.id == int(user_id))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exeption
    return user
