import random
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import DBBookings, DBUser, DBFlight
from app.schemas import Booking
from app.security import get_current_user
from app.database import get_db


router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("/", response_model = list[Booking])
async def get_bookings(db:AsyncSession = Depends(get_db)):
    query = select(DBBookings)
    result = await db.execute(query)
    bookings = result.scalars().all()
    return bookings


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

    flight.remaining_seats = flight.remaining_seats - 1

    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)

    return new_booking

@router.get("/my", response_model = list[Booking])
async def get_my_bookings(current_user:DBUser = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    query = select(DBBookings).where(DBBookings.user_id == current_user.id)
    result = await db.execute(query)

    return result.scalars().all()