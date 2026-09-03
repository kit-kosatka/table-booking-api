from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.repositories.booking import BookingRepository
from app.schemas.booking import BookingCreate, BookingOut
from app.services.booking import create_booking_service


router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)


@router.post(
    "",
    response_model=BookingOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_booking(
    booking_data: BookingCreate,
    session: AsyncSession = Depends(get_db),
) -> BookingOut:
    repository = BookingRepository(session)

    try:
        booking = await create_booking_service(
            repository,
            booking_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return booking