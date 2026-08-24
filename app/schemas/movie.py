from pydantic import BaseModel, Field

class MovieCreate(BaseModel):
    name: str
    language: str
    duration: int = Field(gt = 0)

class MovieUpdate(BaseModel):
    name: str
    language: str
    duration: int = Field(gt = 0)

class MovieResponse(BaseModel):
    id: int
    name: str
    language: str
    duration: int

    class Config:
        from_attributes = True  # from_attributes = True allows Pydantic to convert a SQLAlchemy object into the response schema.
        """
        SQLAlchemy Movie object
                ↓
        Pydantic MovieResponse
                ↓
        JSON
        """