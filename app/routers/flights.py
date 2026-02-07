from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import DBFlight, DBUser
from app.schemas import Flight, FlightCreate, FlightUpdate
from app.security import get_current_user, verify_admin
from app.database import get_db


router = APIRouter(prefix="/flights", tags=["Flights"])

@router.get("/",response_model=list[Flight])
async def get_flights(db:AsyncSession = Depends(get_db)):
    query = select(DBFlight)
    result = await db.execute(query)
    flights = result.scalars().all()
    return flights


@router.post("/")
async def create_flight(flight_data:FlightCreate, db:AsyncSession = Depends(get_db), current_user: DBUser = Depends(get_current_user), admin:DBUser = Depends(verify_admin)):

    departure_naive = flight_data.departure_time.replace(tzinfo=None)
    arrival_naive = flight_data.arrival_time.replace(tzinfo=None)

    new_flight = DBFlight(
        flight_number= flight_data.flight_number,
        departure_city = flight_data.departure_city,
        arrival_city = flight_data.arrival_city,
        departure_time = departure_naive,
        arrival_time = arrival_naive,
        price = flight_data.price,
        remaining_seats = flight_data.remaining_seats,
    )

    db.add(new_flight)
    await db.commit()
    await db.refresh(new_flight)
    return new_flight


@router.patch("/{flight_id}")
async def update_flight(flight_id:int, flight_data:FlightUpdate, current_user:DBUser = Depends(get_current_user), db:AsyncSession = Depends(get_db),admin:DBUser = Depends(verify_admin)):
    query = select(DBFlight).where(DBFlight.id == flight_id)
    result = await db.execute(query)
    flight = result.scalar_one_or_none()

    if not flight:
        raise HTTPException(status_code=404,detail="Рейс не найден")

    update_data = flight_data.model_dump(exclude_unset=True)

    for key,value in update_data.items():
        if isinstance(value, datetime):
            value = value.replace(tzinfo=None)
        setattr(flight,key,value)

    await db.commit()
    await db.refresh(flight)
    return flight


@router.delete("/{flight_id}")
async def delete_flight(flight_id:int, current_user:DBUser = Depends(get_current_user), db:AsyncSession = Depends(get_db), admin:DBUser = Depends(verify_admin)):
    query = select(DBFlight).where(DBFlight.id == flight_id)
    result = await db.execute(query)
    flight = result.scalar_one_or_none()

    if not flight:
        raise HTTPException(status_code=404, detail="Рейс не найден")

    await db.delete(flight)
    await db.commit()
    return {"status": "success", "message": f"Рейс {flight} удален"}