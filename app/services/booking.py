from datetime import date

from app.models.booking import Booking
from app.repositories.booking import BookingRepository
from app.schemas.booking import BookingCreate


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


async def get_booking_by_id_service(
    repository: BookingRepository,
    booking_id: int,
) -> Booking:
    booking = await repository.get_by_id(booking_id)

    if booking is None:
        raise ValueError("Booking not found")

    return booking


async def cancel_booking_service(
    repository: BookingRepository,
    booking_id: int,
) -> Booking:
    booking = await repository.get_by_id(booking_id)

    if booking is None:
        raise ValueError("Booking not found")

    if booking.status == "cancelled":
        raise ValueError("Booking is already cancelled")

    return await repository.cancel(booking)

