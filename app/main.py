from fastapi import FastAPI

from app.api.routes.bookings import router as booking_router

app = FastAPI()

app.include_router(booking_router)
