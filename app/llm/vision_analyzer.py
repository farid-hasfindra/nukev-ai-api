import base64
import logging
from groq import Groq
from app.core.config import settings

logger = logging.getLogger(__name__)

class VisionAnalyzer:
    def __init__(self, model_name: str = "llama-3.2-11b-vision-preview"):
        self.model_name = model_name
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    async def identify_movie_from_image(self, base64_image: str) -> str:
        """
        Menganalisis gambar menggunakan Groq Vision untuk mendapatkan Judul Film/Seri.
        """
        try:
            prompt = """
            Analyze this image and identify the title of the movie, TV series, or anime it represents. 
            If it's a poster, screenshot, or related art, return ONLY the official title of the movie/show.
            If you are unsure, provide your best guess.
            Format your response as a simple string, for example: "Interstellar" or "One Piece".
            If you cannot identify any movie/show, respond with "Unknown".
            """

            # Note: Groq expects the base64 string directly in the content block for vision models
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ],
                temperature=0.1,
                max_tokens=50
            )

            title = response.choices[0].message.content.strip()
            # Clean up potential quotes or extra text
            title = title.replace('"', '').replace("'", "")
            return title

        except Exception as e:
            logger.error(f"Error in Vision Analysis: {e}")
            return "Unknown"

vision_analyzer = VisionAnalyzer()
