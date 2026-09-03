from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date as date_type
from app.api.dependencies import get_db
from app.repositories.booking import BookingRepository
from app.schemas.booking import BookingCreate, BookingOut
from app.services.booking import (
    create_booking_service,
    get_bookings_service,
    get_booking_by_id_service,
    cancel_booking_service,
)

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


@router.get(
    "",
    response_model=list[BookingOut],
)
async def get_bookings(
    date: date_type | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
) -> list[BookingOut]:
    repository = BookingRepository(session)

    return await get_bookings_service(
        repository,
        date,
        page,
        limit,
    )


@router.get(
    "/{booking_id}",
    response_model=BookingOut,
)
async def get_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_db),
) -> BookingOut:
    repository = BookingRepository(session)

    try:
        return await get_booking_by_id_service(
            repository,
            booking_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{booking_id}",
    response_model=BookingOut,
)
async def cancel_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_db),
) -> BookingOut:
    repository = BookingRepository(session)

    try:
        return await cancel_booking_service(
            repository,
            booking_id,
        )
    except ValueError as exc:
        if str(exc) == "Booking not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
