from pydantic import BaseModel
from typing import Optional

class MediaAnalyzeRequest(BaseModel):
    image_base64: str

class MediaAnalyzeResponse(BaseModel):
    title: str
    synopsis: Optional[str] = None
    release_date: Optional[str] = None
    poster_url: Optional[str] = None
    success: bool
    message: Optional[str] = None
