import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class TMDBService:
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {settings.TMDB_READ_ACCESS_TOKEN}"
        }

    async def search_movie(self, title: str):
        """
        Mencari film berdasarkan judul dan mengembalikan detail sinopsis.
        """
        try:
            async with httpx.AsyncClient() as client:
                # Search for the movie
                response = await client.get(
                    f"{self.base_url}/search/movie",
                    headers=self.headers,
                    params={"query": title, "language": "id-ID", "include_adult": "false"}
                )
                response.raise_for_status()
                data = response.json()

                if not data.get("results"):
                    # Fallback ke pencarian bahasa Inggris jika Indonesia kosong
                    response = await client.get(
                        f"{self.base_url}/search/movie",
                        headers=self.headers,
                        params={"query": title, "language": "en-US", "include_adult": "false"}
                    )
                    data = response.json()

                if data.get("results"):
                    top_result = data["results"][0]
                    return {
                        "title": top_result.get("title"),
                        "original_title": top_result.get("original_title"),
                        "synopsis": top_result.get("overview"),
                        "release_date": top_result.get("release_date"),
                        "poster_path": f"https://image.tmdb.org/t/p/w500{top_result.get('poster_path')}" if top_result.get("poster_path") else None,
                        "tmdb_id": top_result.get("id")
                    }
                
                return None
        except Exception as e:
            logger.error(f"Error searching TMDB: {e}")
            return None

tmdb_service = TMDBService()
