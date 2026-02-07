from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import DBFlight, DBUser
from app.schemas import Flight, FlightCreate
from app.security import get_current_user
from app.database import get_db


router = APIRouter(prefix="/flights", tags=["Flights"])

@router.get("/",response_model=list[Flight])
async def get_flights(db:AsyncSession = Depends(get_db)):
    query = select(DBFlight)
    result = await db.execute(query)
    flights = result.scalars().all()
    return flights

@router.post("/")
async def create_flight(flight_data:FlightCreate, db:AsyncSession = Depends(get_db),current_user: DBUser = Depends(get_current_user)):

    if not current_user.is_admin:
        raise HTTPException(status_code=403,detail="Только админ может добавлять рейсы")

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