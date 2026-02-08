from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import DBUser
from app.schemas import UserOut
from app.schemas.user import UserUpdate
from app.security import get_current_user, verify_admin, hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model = list[UserOut])
async def get_users(db:AsyncSession = Depends(get_db), admin:DBUser = Depends(verify_admin)):
    query = select(DBUser)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/{user_id}")
async def update_user(user_id:int,user_data:UserUpdate,current_user:DBUser = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    query = select(DBUser).where(DBUser.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404,detail="Пользователь не найден")

    if not current_user.is_admin and current_user.id != user_id :
        raise HTTPException(status_code=403, detail="Нельзя изменить чужой аккаунт")

    update_data = user_data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    if "is_admin" in update_data and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Только администратор может изменять права доступа")

    for key,value in update_data.items():
        setattr(user,key,value)

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}")
async def delete_user(user_id:int,current_user:DBUser = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    query = select(DBUser).where(DBUser.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if current_user.id == user_id and current_user.is_admin:
        raise HTTPException(status_code=400, detail="Нельзя удалить собственный аккаунт администратора")

    if not current_user.is_admin and current_user.id != user_id :
        raise HTTPException(status_code=403, detail="Нельзя удалить чужой аккаунт")

    await db.delete(user)
    await db.commit()
    return {"status": "success", "message": f"Пользователь {user_id} удален"}