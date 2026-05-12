import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-1.5-flash"
)

TOP_K = int(
    os.getenv("TOP_K", 3)
)

MEMORY_LIMIT = int(
    os.getenv("MEMORY_LIMIT", 100)
)

MAX_INPUT_LENGTH = int(
    os.getenv(
        "MAX_INPUT_LENGTH",
        2000
    )
)

MAX_TOOL_ITERATIONS = int(
    os.getenv(
        "MAX_TOOL_ITERATIONS",
        5
    )
)

DATA_DIRECTORY = os.getenv(
    "DATA_DIRECTORY",
    "data"
)

MEMORY_SIMILARITY_THRESHOLD = float(
    os.getenv(
        "MEMORY_SIMILARITY_THRESHOLD",
        1.5
    )
)

MAX_GEMINI_RETRIES = int(
    os.getenv(
        "MAX_GEMINI_RETRIES",
        3
    )
)
