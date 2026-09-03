import re
from datetime import date, time, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BookingCreate(BaseModel):
    name: str = Field(min_length=2)
    phone: str
    booking_date: date
    booking_time: time
    guests: int = Field(ge=1, le=12)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 2:
            raise ValueError("Имя должно содержать минимум 2 символа")

        if not re.fullmatch(r"[А-Яа-яЁёA-Za-z -]+", value):
            raise ValueError("Имя может содержать только буквы, пробелы и дефис")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not (re.fullmatch(r"\+7\d{10}", value) or re.fullmatch(r"8\d{10}", value)):
            raise ValueError(
                "Телефон должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX"
            )

        return value

    @field_validator("booking_date")
    @classmethod
    def validate_booking_date(cls, value: date) -> date:
        today = date.today()
        max_date = today + timedelta(days=90)

        if not today <= value <= max_date:
            raise ValueError(
                "Дата бронирования должна быть от сегодня до 90 дней вперёд"
            )

        return value

    @field_validator("booking_time")
    @classmethod
    def validate_booking_time(cls, value: time) -> time:
        if (
            value.minute != 0
            or value.second != 0
            or value.microsecond != 0
            or not 12 <= value.hour <= 22
        ):
            raise ValueError(
                "Время бронирования должно быть с 12:00 до 22:00 с шагом 1 час"
            )

        return value


class BookingOut(BookingCreate):
    id: int
    status: Literal["active", "cancelled"]

    model_config = ConfigDict(from_attributes=True)
