from fastapi import APIRouter, HTTPException
from app.schemas.media import MediaAnalyzeRequest, MediaAnalyzeResponse
from app.llm.vision_analyzer import vision_analyzer
from app.services.tmdb import tmdb_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=MediaAnalyzeResponse)
async def analyze_media_content(request: MediaAnalyzeRequest):
    """
    1. Identifikasi judul film dari gambar (Vision AI).
    2. Cari sinopsis resmi dari TMDB.
    """
    try:
        # Step 1: Vision Analysis
        title = await vision_analyzer.identify_movie_from_image(request.image_base64)
        
        if title == "Unknown" or not title:
            return MediaAnalyzeResponse(
                title="Unknown",
                success=False,
                message="Gagal mengidentifikasi judul film dari gambar.",
            )

        # Step 2: Fetch Metadata from TMDB
        tmdb_data = await tmdb_service.search_movie(title)
        
        if not tmdb_data:
            return MediaAnalyzeResponse(
                title=title,
                success=True,
                message="Judul terdeteksi, namun data sinopsis tidak ditemukan di TMDB.",
            )

        return MediaAnalyzeResponse(
            title=tmdb_data["title"],
            synopsis=tmdb_data["synopsis"],
            release_date=tmdb_data["release_date"],
            poster_url=tmdb_data["poster_path"],
            success=True
        )

    except Exception as e:
        logger.error(f"Error analyzing media: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during media analysis.")
