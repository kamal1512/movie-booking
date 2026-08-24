import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.cache.redis import redis_client
from app.models.movie import Movie

"""-------------------------------GET----------------------------"""


def get_all_movies(db: Session, language: str | None = None, page: int = 1, page_size: int = 20):
    if language:
        cache_key = f"movies:language:{language}"
    else:
        cache_key = "movies:all"

    cached_movies = redis_client.get(cache_key)

    if cached_movies:
        return json.loads(cached_movies)

    offset = (page -1) * page_size

    query = db.query(Movie).offset(offset).limit(page_size)

    if language:
        query = query.filter(
            Movie.language.ilike(language)
        )
    movies = query.all()

    result = [
        {
            "id": movie.id,
            "name": movie.name,
            "language": movie.language,
            "duration": movie.duration
        } for movie in movies
    ]

    redis_client.setex(
        cache_key,
        60,
        json.dumps(result)
    )

    return result

def get_movie_by_id(db: Session, movie_id: int):
    return db.query(Movie).filter(
        Movie.id == movie_id
    ).first()

def search_movies(db: Session, name: str):
    return db.query(Movie).filter(
        Movie.name.like(f"%{name}")
    ).all()

"""-------------------------------POST----------------------------"""

def create_movie(db: Session, name: str, language: str, duration: int):

    movie = Movie(
        name= name,
        language=language,
        duration=duration
    )

    db.add(movie)   # Add this python object to the current database session
    db.commit()     # persist the transaction to PostgreSQL
    db.refresh(movie)   # refreshes the object with database-generated values (After refresh you will get id field as well)

    redis_client.delete(
        "movies:all"
    )
    redis_client.delete(
        f"movies:language:{language}"
    )

    return movie

def update_movie(db: Session, movie_id: int, name: str, language: str, duration: int):
    movie = get_movie_by_id(db, movie_id)

    if movie is None:
        return None

    movie.name = name
    movie.language = language
    movie.duration = duration

    db.commit()
    db.refresh(movie)

    redis_client.delet("movies:all")

    return movie

def delete_movie(db: Session, movie_id: int):
    movie = get_movie_by_id(db, movie_id)

    if movie is None:
        return False

    db.delete(movie)
    db.commit()

    redis_client.delete("movies:all")

    return True