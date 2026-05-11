from pathlib import Path

from app.config import DATA_DIRECTORY
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FileReaderTool:

    name = "file_reader"

    description = (
        "Reads local text files safely."
    )

    @staticmethod
    def execute(file_name: str):

        if not file_name or not file_name.strip():

            return {
                "success": False,
                "output": "empty file name"
            }

        try:

            safe_path = (
                Path(DATA_DIRECTORY) / file_name
            ).resolve()

            data_directory = (
                Path(DATA_DIRECTORY).resolve()
            )

            # Prevent directory traversal
            if not str(safe_path).startswith(
                str(data_directory)
            ):

                return {
                    "success": False,
                    "output": "unsafe file path"
                }

            if not safe_path.exists():

                return {
                    "success": False,
                    "output": "file not found"
                }

            if safe_path.suffix != ".txt":

                return {
                    "success": False,
                    "output": (
                        "only .txt files supported"
                    )
                }

            content = safe_path.read_text(
                encoding="utf-8"
            )

            return {
                "success": True,
                "output": content
            }

        except Exception as e:

            logger.error(
                f"File reader failed: {e}"
            )

            return {
                "success": False,
                "output": str(e)
            }
