import random
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import DBBookings, DBUser, DBBookings, DBFlight
from app.schemas import Booking, BookingUpdate
from app.security import get_current_user, verify_admin
from app.database import get_db


router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("/", response_model = list[Booking])
async def get_bookings(db:AsyncSession = Depends(get_db), admin:DBUser = Depends(verify_admin)):
    query = select(DBBookings)
    result = await db.execute(query)
    bookings = result.scalars().all()
    return bookings


@router.get("/my", response_model = list[Booking])
async def get_my_bookings(current_user:DBUser = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    query = select(DBBookings).where(DBBookings.user_id == current_user.id)
    result = await db.execute(query)

    return result.scalars().all()


@router.post("/")
async def create_booking(flight_id:int,current_user: DBUser = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    query = select(DBFlight).where(DBFlight.id == flight_id)
    result = await db.execute(query)
    flight = result.scalar_one_or_none()

    if not flight:
        raise HTTPException(status_code=404, detail="Рейс не найден")

    if flight.remaining_seats <=0:
        raise HTTPException(status_code=400, detail="Мест нет")

    new_booking = DBBookings(
        user_id = current_user.id,
        flight_id = flight.id,
        ticket_number = "UN " + str(random.randint(1000,2000)),
        booking_date = datetime.now(timezone.utc).replace(tzinfo=None)
    )

    flight.remaining_seats -= 1

    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)

    return new_booking


@router.patch("/{booking_id}")
async def update_booking(booking_id:int,booking_data:BookingUpdate,current_user:DBUser = Depends(get_current_user),db:AsyncSession = Depends(get_db), admin:DBUser = Depends(verify_admin)):
    query = select(DBBookings).where(DBBookings.id == booking_id)
    result = await db.execute(query)
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404,detail="Бронь не найдена")

    update_data = booking_data.model_dump(exclude_unset=True)

    for key,value in update_data.items():
        if isinstance(value, datetime):
            value = value.replace(tzinfo=None)
        setattr(booking ,key,value)

    await db.commit()
    await db.refresh(booking)
    return booking


@router.delete("/{booking_id}")
async def delete_booking(booking_id:int,current_user:DBUser = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    query = select(DBBookings).where(DBBookings.id == booking_id)
    result = await db.execute(query)
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Бронь не найдена")

    if not current_user.is_admin and booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нельзя удалить чужую бронь")

    query = select(DBFlight).where(DBFlight.id == booking.flight_id)
    result = await db.execute(query)
    flight = result.scalar_one_or_none()

    if not flight:
        raise HTTPException(status_code=404, detail="Рейс не найден")

    flight.remaining_seats += 1

    await db.delete(booking)
    await db.commit()
    return {"status": "success", "message": f"Бронь {booking} удалена"}