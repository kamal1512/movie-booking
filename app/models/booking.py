from datetime import datetime, timezone

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

from app.db.database import Base

class Booking(Base):

    __tablename__ = "bookings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    movie_id = Column(
        Integer,
        ForeignKey("movies.id"),
        nullable=False
    )

    seats = Column(
        Integer,
        nullable=False
    )

    total_price = Column(
        Integer,
        nullable=False
    )

    status = Column(
        String,
        default="Confirmed",
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )