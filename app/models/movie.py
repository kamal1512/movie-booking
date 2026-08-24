from sqlalchemy import Column, Integer, String

from app.db.database import Base

class Movie(Base):

    __tablename__ = "movies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    language = Column(
        String,
        nullable=False
    )

    duration = Column(
        Integer,
        nullable=False
    )