from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers.users import router as users_router
from app.routers.flights import router as flights_router
from app.routers.bookings import router as bookings_router
from app.routers.auth import router as auth_router

app = FastAPI(redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342", "http://127.0.0.1:63342"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(flights_router)
app.include_router(bookings_router)
app.include_router(auth_router)