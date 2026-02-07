from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.flights import router as flights_router
from app.routers.bookings import router as bookings_router
from app.routers.auth import router as auth_router

app = FastAPI()

app.include_router(users_router)
app.include_router(flights_router)
app.include_router(bookings_router)
app.include_router(auth_router)