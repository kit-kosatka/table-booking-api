from app.models.booking import Booking
from app.repositories.booking import BookingRepository
from app.schemas.booking import BookingCreate
from datetime import date


async def create_booking_service(
    repository: BookingRepository,
    booking_data: BookingCreate,
) -> Booking:
    existing_booking = await repository.get_active_booking_by_slot(
        booking_data.booking_date,
        booking_data.booking_time,
    )

    if existing_booking:
        raise ValueError("Booking slot is already occupied")

    return await repository.create(booking_data)

async def get_bookings_service(
    repository: BookingRepository,
    booking_date: date | None = None,
) -> list[Booking]:
    return await repository.get_all(booking_date)
