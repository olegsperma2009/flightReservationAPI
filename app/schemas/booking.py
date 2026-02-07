from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class BookingBase(BaseModel):
    user_id:int
    flight_id:int

class Booking(BookingBase):
    id: int
    ticket_number: str = Field(..., min_length=6, max_length=7)
    booking_date: datetime
    status: Optional[str]

    model_config = ConfigDict(from_attributes=True)