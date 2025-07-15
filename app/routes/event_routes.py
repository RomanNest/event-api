from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_async_session
from app.schemas import EventCreate, EventOut, BookingRequest
from app.auth.dependencies import get_current_user_id
from app.crud import (
    create_event,
    get_events,
    get_user_events,
    get_total_booked_seats,
    get_booking_by_user_and_event,
    get_event,
    create_booking,
)

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/", response_model=List[EventOut])
async def read_events(db: AsyncSession = Depends(get_async_session)):
    """List of all events is public"""
    return await get_events(db)


@router.post("/", response_model=EventOut)
async def create_new_event(
    event_data: EventCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_session),
):
    """Event creation - secure route"""
    return await create_event(db, event_data, current_user_id)


@router.get("/my", response_model=List[EventOut])
async def read_my_events(
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_session),
):
    """List of your events — a protected route"""
    return await get_user_events(db, current_user_id)


@router.post("/{event_id}/book")
async def book_seats(
    event_id: int,
    booking_request: BookingRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_session),
):
    seats_booked = booking_request.seats_booked
    """Book your event seats - secure route"""
    event = await get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check if the user has already booked this event
    existing_booking = await get_booking_by_user_and_event(
        db, current_user_id, event_id
    )
    if existing_booking:
        raise HTTPException(
            status_code=400, detail="You have already booked this event"
        )

    # Checking the number of available seats
    total_booked = await get_total_booked_seats(db, event_id)
    available_seats = event.max_seats - total_booked
    if seats_booked > available_seats:
        raise HTTPException(
            status_code=400, detail="Not enough seats available"
        )

    # Creating a reservation
    booking = await create_booking(db, current_user_id, event_id, seats_booked)
    return {"status": "Booking created", "booking_id": booking.id}
