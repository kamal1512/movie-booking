from pydantic import BaseModel, Field
from datetime import  datetime

class BookingCreate(BaseModel):
    movie_id: int
    seats:int = Field(gt=0, le=10)

class BookingResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    seats: int
    total_price: int
    status: str
    created_at: datetime

    class Config:
        from_attributes=True