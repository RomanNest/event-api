from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Event, Booking
from app.schemas import UserCreate, EventCreate


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def create_user(
    db: AsyncSession, user_create: UserCreate, hashed_password: str
) -> User:
    db_user = User(
        email=user_create.email,
        password_hash=hashed_password,
        name=user_create.name,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_events(db: AsyncSession) -> list[Event]:
    result = await db.execute(select(Event))
    return list(result.scalars().all())


async def get_event(db: AsyncSession, event_id: int) -> Event | None:
    result = await db.execute(select(Event).filter(Event.id == event_id))
    return result.scalars().first()


async def create_event(
    db: AsyncSession, event_create: EventCreate, owner_id: int
) -> Event:
    db_event = Event(
        title=event_create.title,
        description=event_create.description,
        datetime=event_create.datetime,
        max_seats=event_create.max_seats,
        owner_id=owner_id,
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


async def get_user_bookings(db: AsyncSession, user_id: int) -> list[Booking]:
    result = await db.execute(
        select(Booking).filter(Booking.user_id == user_id)
    )
    return list(result.scalars().all())


async def create_booking(
    db: AsyncSession, user_id: int, event_id: int, seats_booked: int
) -> Booking:
    db_booking = Booking(
        user_id=user_id, event_id=event_id, seats_booked=seats_booked
    )
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)
    return db_booking


async def get_booking_by_user_and_event(
    db: AsyncSession, user_id: int, event_id: int
) -> Booking | None:
    result = await db.execute(
        select(Booking).filter(
            Booking.user_id == user_id, Booking.event_id == event_id
        )
    )
    return result.scalars().first()


async def get_user_events(db: AsyncSession, user_id: int) -> list[Event]:
    result = await db.execute(select(Event).filter(Event.owner_id == user_id))
    return list(result.scalars().all())


async def get_total_booked_seats(db: AsyncSession, event_id: int) -> int:
    result = await db.execute(
        select(func.sum(Booking.seats_booked)).filter(
            Booking.event_id == event_id
        )
    )
    total = result.scalar()
    return total or 0
