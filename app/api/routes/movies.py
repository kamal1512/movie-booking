import time

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.dependencies import get_async_db
from app.db.session import get_db
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieResponse, MovieUpdate
from app.services import  movie_service
from app.cache.redis import redis_client
from app.services.external_movie_service import get_external_movie

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)
"""-------------------------------Temporary----------------------------"""

@router.get("/redis-test")
def redis_test():
    redis_client.set(
        "hello",
        "Hello Redis!"
    )

    value = redis_client.get("hello")

    return {"value": value}

@router.get("/external/{movie_id}")
async def external_movie(movie_id: int):

    movie = await get_external_movie(movie_id)

    return movie

"""-------------------------------GET----------------------------"""
@router.get("")
async def get_movies(language: str, db: AsyncSession = Depends(get_async_db)):
    """Asynchronous endpoint and db call to get movies"""
    start_time = time.perf_counter()

    result = await db.execute(
        select(Movie).where(Movie.language == language)
    )
    movies = result.scalars().all()

    total_time = (time.perf_counter() - start_time) * 1000
    logger.info("GET MOVIES TOOK %.2fms", total_time)

    return movies

# @router.get("/")
# def get_movies(language: str | None = None, db: Session = Depends(get_db), page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
#     """
#     Depends(get_db) - Dependency Injection
#                         We don't have to manually write db = SessionLocal() inside every endpoint
#     """
#     start_time = time.perf_counter()
#     movies = movie_service.get_all_movies(db, language, page, page_size)
#     total_time = (time.perf_counter() - start_time) * 1000
#
#     logger.info("GET MOVIES TOOK %.2fms", total_time)
#
#     return movies
@router.get("/pagination")
def get_movies_pagination(
    page: int = Query(1, ge=1),
    page_size: int = Query(
        20,
        ge=1,
        le=100
    ),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size

    return (
        db.query(Movie)
        .offset(offset)
        .limit(page_size)
        .all()
    )
@router.get("/search")
def search_movies(name: str, db: Session = Depends(get_db)):
    return movie_service.search_movies(db, name)

# @router.get("/{movie_id}")
# def get_movie(movie_id: int, db: Session = Depends(get_db)):
#     movie = movie_service.get_movie_by_id(db, movie_id)
#     if movie is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Movie not found..."
#         )
#     return movie

@router.get("/{movie_id}")
async def get_movie(
    movie_id: int,
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(
        select(Movie).where(Movie.id == movie_id)
    )

    movie = result.scalar_one_or_none()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    return movie

"""-------------------------------POST----------------------------"""
@router.post("/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    return movie_service.create_movie(
        db,
        movie.name,
        movie.language,
        movie.duration
    )

"""-------------------------------PUT----------------------------"""
@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    updated_movie = movie_service.update_movie(
        db,
        movie_id,
        movie.name,
        movie.language,
        movie.duration
    )

    if updated_movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )

    return updated_movie

"""-------------------------------DELETE----------------------------"""
@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    deleted = movie_service.delete_movie(db, movie_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    return {
        "message": "Movie deleted successfully"
    }


@router.get("/slow-db")
def slow_db(name: str, db: Session = Depends(get_db)):
    from app.models.movie import Movie
    time.sleep(3)

    movies = db.query(Movie).all()

    result = [
        movie
        for movie in movies
        if name.lower() in movie.name.lower()
    ]

    return result