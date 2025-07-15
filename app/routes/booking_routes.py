from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_async_session
from app.schemas import BookingOut
from app.crud import get_user_bookings
from app.auth.dependencies import get_current_user_id

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/my", response_model=List[BookingOut])
async def read_my_bookings(
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_session),
):
    return await get_user_bookings(db, current_user_id)
