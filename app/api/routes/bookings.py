import time

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.booking import BookingResponse, BookingCreate
from app.models.user import User
from app.services import booking_service


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
        POST /bookings
           │
           ├── get_current_user()
           │       ↓
           │     JWT
           │       ↓
           │     User
           │
           ├── get_db()
           │       ↓
           │     DB Session
           │
           ▼
        create_booking()
    """
    result = booking_service.create_booking(
        db=db,
        user_id=current_user.id,
        movie_id=booking.movie_id,
        seats=booking.seats
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )

    return result

@router.get("/", response_model=list[BookingResponse])
def get_my_bookings(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
        JWT
         ↓
        user_id = 1
         ↓
        SELECT *
        FROM bookings
        WHERE user_id = 1
    """
    return booking_service.get_user_bookings(
        db=db,
        user_id=current_user.id
    )


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
        booking_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    booking = booking_service.get_booking(db, booking_id, current_user.id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    return booking

@router.delete("/{booking_id}")
def delete_booking(booking_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted = booking_service.delete_booking(
        db=db,
        booking_id=booking_id,
        user_id=current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    return {
        "message": "Booking cancelled successfully"
    }
