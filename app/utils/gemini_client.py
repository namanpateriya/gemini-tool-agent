import json
import time

import google.generativeai as genai

from app.config import (
    GEMINI_API_KEY,
    MODEL_NAME,
    MAX_GEMINI_RETRIES
)

from app.utils.logger import (
    get_logger
)

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

            self.model = (
                genai.GenerativeModel(
                    MODEL_NAME
                )
            )

            logger.info(
                f"Gemini initialized "
                f"with model: {MODEL_NAME}"
            )

        except Exception as e:

            logger.error(
                f"Gemini init failed: {e}"
            )

    def generate(
        self,
        prompt: str
    ):

        if self.model is None:

            return (
                "error: Gemini model "
                "not initialized"
            )

        last_error = None

        for attempt in range(
            MAX_GEMINI_RETRIES
        ):

            try:

                response = (
                    self.model.generate_content(
                        prompt
                    )
                )

                if (
                    hasattr(response, "text")
                    and response.text
                ):

                    return (
                        response.text.strip()
                    )

                last_error = (
                    "empty response"
                )

            except Exception as e:

                last_error = str(e)

                logger.error(
                    f"Gemini attempt "
                    f"{attempt + 1} failed: "
                    f"{e}"
                )

                time.sleep(1)

        return f"error: {last_error}"

    def generate_json(
        self,
        prompt: str
    ):

        response = self.generate(
            prompt
        )

        if response.startswith(
            "error:"
        ):

            return {
                "status": "error",
                "message": response
            }

        try:

            cleaned = (
                response
                .replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
                .strip()
            )

            parsed = json.loads(
                cleaned
            )

            return {
                "status": "success",
                "data": parsed
            }

        except Exception as e:

            logger.error(
                f"JSON parse failed: {e}"
            )

            return {
                "status": "error",
                "message": (
                    "invalid json response"
                ),
                "raw_response": response
            }
