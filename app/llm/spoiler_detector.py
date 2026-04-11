import json
import logging
from groq import Groq
from app.core.config import settings
from app.schemas.comment import CommentValidateResponse

logger = logging.getLogger(__name__)

class SpoilerDetector:
    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        self.model_name = model_name
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def analyze_comment(self, video_context: str, comment_text: str) -> dict:
        prompt = f"""
        You are an advanced AI content moderator responsible for detecting movie spoilers in user comments to protect the user experience on a video platform called 'Nukev'.

        Analyze the following user comment based on the provided content metadata (Title & Synopsis). 
        Use the 'Content Context' as your Ground Truth. Any revelation of key plot points, twists, endings, or character fates mentioned in the context (but not known at the start of the story) should be classified as a spoiler.

        Content Context: "{video_context}"
        User Comment: "{comment_text}"

        Important rules for classifying a spoiler:
        1. Plot reveals: Giving away the ending, a major plot twist, who lives/dies, or significant unexpected events.
        2. Character arcs: Revealing significant transformations or hidden identities not known early in the story.
        3. Cameos/Surprises: Revealing hidden characters or actors that appear without prior public announcement.
        4. If a comment is just an opinion (e.g., "The movie is bad") without specific plot details, it is NOT a spoiler.
        5. If the comment discusses widely known facts from the trailer, it is probably NOT a spoiler, unless it connects them in a revealing way.

        Respond strictly in JSON format matching this structure:
        {{
            "is_spoiler": true or false,
            "confidence_score": a float between 0.0 and 1.0,
            "reason": "short explanation"
        }}
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a JSON-only response bot. You always output valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            result_json = json.loads(response.choices[0].message.content)
            
            # Ensure safe fallback for fields
            return {
                "is_spoiler": bool(result_json.get("is_spoiler", False)),
                "confidence_score": float(result_json.get("confidence_score", 0.0)),
                "reason": str(result_json.get("reason", "Could not analyze format."))
            }
            
        except Exception as e:
            logger.error(f"Error during Groq AI generation: {e}", exc_info=True)
            # Fallback error behavior
            return {
                "is_spoiler": False, 
                "confidence_score": 0.0, 
                "reason": "Error connecting to AI service."
            }
