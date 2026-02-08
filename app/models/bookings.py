from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class DBBookings(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String)
    user_id = Column(Integer,ForeignKey("users.id"))
    flight_id = Column(Integer,ForeignKey("flights.id"))
    booking_date = Column(default=datetime.now(timezone.utc).replace(tzinfo=None))
    status = Column(String)

    user = relationship("DBUser", back_populates="bookings", cascade="all, delete-orphan")
    flight = relationship("DBFlight", back_populates="bookings", cascade="all, delete-orphan")