from fastapi import APIRouter, HTTPException, Depends
from app.schemas.comment import CommentValidateRequest, CommentValidateResponse
from app.llm.spoiler_detector import SpoilerDetector
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Dependency injection for the detector
def get_detector():
    return SpoilerDetector()

@router.post("/validate-spoiler", response_model=CommentValidateResponse)
async def validate_comment_spoiler(
    request: CommentValidateRequest, 
    detector: SpoilerDetector = Depends(get_detector)
):
    try:
        result = detector.analyze_comment(
            video_context=request.video_context,
            comment_text=request.comment_text
        )
        return CommentValidateResponse(**result)
    except Exception as e:
        logger.error(f"Failed to analyze spoiler: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during spoiler validation.")
