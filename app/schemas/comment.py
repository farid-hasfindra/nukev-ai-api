from pydantic import BaseModel, Field

class CommentValidateRequest(BaseModel):
    video_context: str = Field(..., description="The context or topic of the video (e.g., 'Review of Avengers Endgame', 'Spiderman No Way Home ending explanation').")
    comment_text: str = Field(..., description="The user's comment to validate for spoilers.")

class CommentValidateResponse(BaseModel):
    is_spoiler: bool = Field(..., description="True if the comment contains a spoiler based on the video context, False otherwise.")
    confidence_score: float = Field(..., description="Confidence score between 0.0 and 1.0 that this assessment is correct.")
    reason: str = Field(..., description="A short explanation of why the comment was classified as a spoiler or not.")
