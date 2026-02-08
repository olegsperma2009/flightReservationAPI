from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator, Field


class FlightBase(BaseModel):
    flight_number: str
    departure_city: str
    arrival_city: str
    departure_time: datetime
    arrival_time: datetime
    price: int = Field(..., gt=0)
    remaining_seats: int = Field(..., ge=0)

    @model_validator(mode="after")
    def check_arrival_after_departure(self):
        if self.arrival_time <= self.departure_time:
            raise ValueError("Время прилёта должно быть позже времени вылета")
        return self

class FlightCreate(FlightBase):
    pass


class FlightUpdate(BaseModel):
    flight_number: Optional[str] = None
    departure_city: Optional[str] = None
    arrival_city: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    price: Optional[int] = Field(None, gt=0)
    remaining_seats: Optional[int] = Field(None, gt=0)

    @model_validator(mode="after")
    def check_arrival_after_departure(self):
        if self.arrival_time and self.departure_time:
            if self.arrival_time <= self.departure_time:
                raise ValueError("Время прилёта должно быть позже времени вылета")
        return self

class Flight(FlightBase):
    id:int

    model_config = ConfigDict(from_attributes=True)