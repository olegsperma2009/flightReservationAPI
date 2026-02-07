from datetime import datetime
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

class Flight(FlightBase):
    id:int

    model_config = ConfigDict(from_attributes=True)