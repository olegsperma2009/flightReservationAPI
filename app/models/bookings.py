from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class DBBookings(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String)
    user_id = Column(Integer,ForeignKey("users.id"))
    user = relationship("DBUser", back_populates="bookings")
    flight_id = Column(Integer,ForeignKey("flights.id"))
    flight = relationship("DBFlight", back_populates="bookings")
    booking_date = Column(DateTime)
    status = Column(String)