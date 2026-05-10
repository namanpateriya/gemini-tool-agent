import json
import google.generativeai as genai

from app.config import (
    GEMINI_API_KEY,
    MODEL_NAME
)

from app.utils.logger import get_logger

logger = get_logger(__name__)


class GeminiClient:

    def __init__(self):

        self.model = None

        if not GEMINI_API_KEY:
            logger.warning(
                "Missing GEMINI_API_KEY"
            )
            return

        try:
            genai.configure(
                api_key=GEMINI_API_KEY
            )

            self.model = genai.GenerativeModel(
                MODEL_NAME
            )

            logger.info(
                f"Gemini initialized with model: {MODEL_NAME}"
            )

        except Exception as e:
            logger.error(
                f"Gemini initialization failed: {e}"
            )

    def generate(self, prompt: str):

        if self.model is None:
            return "error: Gemini model not initialized"

        try:

            response = self.model.generate_content(
                prompt
            )

            if (
                hasattr(response, "text")
                and response.text
            ):
                return response.text.strip()

            return "error: empty response"

        except Exception as e:

            logger.error(
                f"Gemini generation failed: {e}"
            )

            return f"error: {str(e)}"

    def generate_json(self, prompt: str):

        response = self.generate(prompt)

        if response.startswith("error:"):
            return {
                "status": "error",
                "message": response
            }

        try:
            cleaned = (
                response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            parsed = json.loads(cleaned)

            return {
                "status": "success",
                "data": parsed
            }

        except Exception as e:

            logger.error(
                f"JSON parsing failed: {e}"
            )

            return {
                "status": "error",
                "message": "invalid json response",
                "raw_response": response
            }
