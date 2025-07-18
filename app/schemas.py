from datetime import datetime
from pydantic import BaseModel, EmailStr, constr


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=128)
    name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class EventBase(BaseModel):
    title: str
    description: str | None = None
    datetime: datetime
    max_seats: int


class EventCreate(EventBase):
    pass


class EventOut(EventBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    seats_booked: int


class BookingOut(BaseModel):
    id: int
    user_id: int
    event_id: int
    seats_booked: int

    class Config:
        from_attributes = True


class BookingRequest(BaseModel):
    seats_booked: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
