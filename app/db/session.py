from sqlalchemy.orm import sessionmaker, Session

from app.db.database import engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    When a request comes in: GET /movies
    Create DB session
           ↓
    Give session to endpoint
           ↓
    Execute query
           ↓
    Close session
    """
    db = SessionLocal()     # Create DB session

    try:
        yield db            # Give session to endpoint
    finally:
        db.close()          # Close session