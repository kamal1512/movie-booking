import httpx

async def get_external_movie(movie_id: int):
    url = f"https://api/example.com/movies/{movie_id}"

    async with httpx.AsyncClient() as client:

        response = await client.get(url, timeout=5.0)

        response.raise_for_status()

        return response.json()