from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    events = relationship("Event", back_populates="owner")
    bookings = relationship("Booking", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    datetime = Column(DateTime, nullable=False)
    max_seats = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="events")
    bookings = relationship("Booking", back_populates="event")

    def __repr__(self):
        return f"<Event(id={self.id}, title={self.title})>"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    seats_booked = Column(Integer, nullable=False)

    user = relationship("User", back_populates="bookings")
    event = relationship("Event", back_populates="bookings")
