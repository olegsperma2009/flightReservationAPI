from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class FlightBase(BaseModel):
    flight_number: str
    departure_city: str
    arrival_city: str
    departure_time: datetime
    arrival_time: datetime
    price: int
    remaining_seats: int


class FlightCreate(FlightBase):
    pass


class FlightUpdate(BaseModel):
    flight_number: Optional[str] = None
    departure_city: Optional[str] = None
    arrival_city: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    price: Optional[int] = None
    remaining_seats: Optional[int] = None


class Flight(FlightBase):
    id:int

    model_config = ConfigDict(from_attributes=True)