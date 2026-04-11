from fastapi import APIRouter
from app.api.v1 import comments, media

api_router = APIRouter()
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(media.router, prefix="/media", tags=["media"])
