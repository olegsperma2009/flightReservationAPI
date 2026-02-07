from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fio = Column(String)
    email = Column(String)
    password = Column(String)
    is_admin = Column(Boolean, default = False)
    bookings = relationship("DBBookings", back_populates="user")