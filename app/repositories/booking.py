from datetime import date, time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.schemas.booking import BookingCreate


class BookingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_active_booking_by_slot(
        self,
        booking_date: date,
        booking_time: time,
    ) -> Booking | None:
        stmt = select(Booking).where(
            Booking.booking_date == booking_date,
            Booking.booking_time == booking_time,
            Booking.status == "active",
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def create(
        self,
        booking_data: BookingCreate,
    ) -> Booking:
        booking = Booking(
            name=booking_data.name,
            phone=booking_data.phone,
            booking_date=booking_data.booking_date,
            booking_time=booking_data.booking_time,
            guests=booking_data.guests,
            status="active",
        )

        self.session.add(booking)
        await self.session.commit()
        await self.session.refresh(booking)

        return booking