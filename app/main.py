from fastapi import FastAPI

from app.db.database import Base, engine

from app.models.movie import Movie
from app.models.user import User
from app.models.booking import Booking

from app.api.routes.movies import router as movie_router
from app.api.routes.users import router as user_router
from app.api.routes.bookings import router as booking_router

from app.middleware.logging import log_request_time

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Booking API",
    description="Backend API for movie ticket booking",
    version="1.0.0"
)

app.middleware("http")(log_request_time)

app.include_router(movie_router)
app.include_router(user_router)
app.include_router(booking_router)

@app.get("/")
def home():
    return {
        "message": "Movie Booking API is running"
    }

