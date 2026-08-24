import time

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.models.booking import Booking
from app.models.movie import Movie

TICKET_PRICE = 250

def create_booking(db: Session, user_id: int, movie_id: int, seats: int):

    start_time = time.perf_counter()

    movie = db.query(Movie).filter(
        Movie.id == movie_id
    ).first()

    db_time = (time.perf_counter() - start_time) * 1000

    logger.info("Movie query took %.2fms", db_time)

    if movie is None:
        return None

    total_price = seats * TICKET_PRICE

    booking = Booking(
        user_id=user_id,
        movie_id=movie_id,
        seats=seats,
        total_price=total_price,
        status="CONFIRMED"
    )

    start_time = time.perf_counter()

    db.add(booking)
    db.commit()
    db.refresh(booking)
    db_time = (time.perf_counter() - start_time) * 1000

    logger.info("Movie Booking insert took %.2fms", db_time)

    return booking

def get_user_bookings(db: Session, user_id: int):
    return db.query(Booking).filter(
        Booking.user_id == user_id
    ).all()

def get_booking(db: Session, booking_id: int, user_id: int):
    return db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == user_id
    ).first()

def delete_booking(db: Session, booking_id: int, user_id: int):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == user_id
    ).first()

    if booking is None:
        return False

    db.delete(booking)
    db.commit()

    return True

def calculate_total_price(seats: int, price_per_seat: int):

    if seats <= 0:
        raise ValueError(
            "Seats must be greater than zero"
        )
    return seats * price_per_seat