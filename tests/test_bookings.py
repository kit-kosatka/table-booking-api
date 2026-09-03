import pytest
from datetime import date, timedelta

@pytest.mark.asyncio
async def test_create_booking(client):
    booking_date = date.today() + timedelta(days=1)

    response = await client.post(
        "/bookings",
        json={
            "name": "Иван Иванов",
            "phone": "+79991234567",
            "booking_date": booking_date.isoformat(),
            "booking_time": "18:00:00",
            "guests": 2,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Иван Иванов"
    assert data["phone"] == "+79991234567"
    assert data["booking_date"] == booking_date.isoformat()
    assert data["booking_time"] == "18:00:00"
    assert data["guests"] == 2
    assert data["status"] == "active"
    assert "id" in data



@pytest.mark.asyncio
async def test_create_booking_conflict(client):
    booking_date = date.today() + timedelta(days=2)

    booking_data = {
        "name": "Петр Петров",
        "phone": "+79991234567",
        "booking_date": booking_date.isoformat(),
        "booking_time": "19:00:00",
        "guests": 2,
    }

    first_response = await client.post(
        "/bookings",
        json=booking_data,
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        "/bookings",
        json=booking_data,
    )

    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "Booking slot is already occupied"
    }


@pytest.mark.asyncio
async def test_get_bookings(client):
    booking_date = date.today() + timedelta(days=3)

    booking_data = {
        "name": "Алексей Смирнов",
        "phone": "+79991234567",
        "booking_date": booking_date.isoformat(),
        "booking_time": "20:00:00",
        "guests": 4,
    }

    create_response = await client.post(
        "/bookings",
        json=booking_data,
    )

    assert create_response.status_code == 201

    response = await client.get("/bookings")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Алексей Смирнов"
    assert data[0]["booking_date"] == booking_date.isoformat()


@pytest.mark.asyncio
async def test_get_bookings_by_date(client):
    target_date = date.today() + timedelta(days=4)
    other_date = date.today() + timedelta(days=5)

    await client.post(
        "/bookings",
        json={
            "name": "Иван Иванов",
            "phone": "+79991234567",
            "booking_date": target_date.isoformat(),
            "booking_time": "18:00:00",
            "guests": 2,
        },
    )

    await client.post(
        "/bookings",
        json={
            "name": "Петр Петров",
            "phone": "+79991234567",
            "booking_date": other_date.isoformat(),
            "booking_time": "19:00:00",
            "guests": 3,
        },
    )

    response = await client.get(
        "/bookings",
        params={"date": target_date.isoformat()},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Иван Иванов"
    assert data[0]["booking_date"] == target_date.isoformat()


@pytest.mark.asyncio
async def test_get_booking_by_id(client):
    booking_date = date.today() + timedelta(days=6)

    create_response = await client.post(
        "/bookings",
        json={
            "name": "Сергей Сергеев",
            "phone": "+79991234567",
            "booking_date": booking_date.isoformat(),
            "booking_time": "18:00:00",
            "guests": 2,
        },
    )

    assert create_response.status_code == 201

    booking_id = create_response.json()["id"]

    response = await client.get(f"/bookings/{booking_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == booking_id
    assert data["name"] == "Сергей Сергеев"
    assert data["status"] == "active"


@pytest.mark.asyncio
async def test_get_booking_not_found(client):
    response = await client.get("/bookings/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Booking not found"
    }


@pytest.mark.asyncio
async def test_cancel_booking(client):
    booking_date = date.today() + timedelta(days=7)

    booking_data = {
        "name": "Анна Антонова",
        "phone": "+79991234567",
        "booking_date": booking_date.isoformat(),
        "booking_time": "20:00:00",
        "guests": 2,
    }

    create_response = await client.post(
        "/bookings",
        json=booking_data,
    )

    assert create_response.status_code == 201

    booking_id = create_response.json()["id"]

    response = await client.delete(f"/bookings/{booking_id}")

    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"

    get_response = await client.get(f"/bookings/{booking_id}")

    assert get_response.status_code == 200
    assert get_response.json()["status"] == "cancelled"


@pytest.mark.asyncio
async def test_cancelled_booking_does_not_block_slot(client):
    booking_date = date.today() + timedelta(days=8)

    booking_data = {
        "name": "Иван Иванов",
        "phone": "+79991234567",
        "booking_date": booking_date.isoformat(),
        "booking_time": "18:00:00",
        "guests": 2,
    }

    create_response = await client.post(
        "/bookings",
        json=booking_data,
    )

    assert create_response.status_code == 201

    booking_id = create_response.json()["id"]

    cancel_response = await client.delete(
        f"/bookings/{booking_id}",
    )

    assert cancel_response.status_code == 200

    second_response = await client.post(
        "/bookings",
        json=booking_data,
    )

    assert second_response.status_code == 201

@pytest.mark.asyncio
async def test_cancel_booking_not_found(client):
    response = await client.delete("/bookings/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Booking not found"
    }