from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import DBUser
from app.schemas import UserOut

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model = list[UserOut])
async def get_users(db:AsyncSession = Depends(get_db)):
    query = select(DBUser)
    result = await db.execute(query)
    users = result.scalars().all()
    return users


