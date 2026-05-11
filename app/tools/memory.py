from app.memory.vector_store import (
    VectorMemoryStore
)

from app.utils.logger import get_logger

logger = get_logger(__name__)

memory_store = VectorMemoryStore()


class MemoryTool:

    name = "memory"

    description = (
        "Stores and retrieves semantic memory."
    )

    @staticmethod
    def store(text: str):

        if not text or not text.strip():

            return {
                "success": False,
                "output": "empty memory"
            }

        memory_store.add_memory(text)

        return {
            "success": True,
            "output": f"stored memory: {text}"
        }

    @staticmethod
    def retrieve(query: str):

        if not query or not query.strip():

            return {
                "success": False,
                "output": []
            }

        results = memory_store.search(query)

        return {
            "success": True,
            "output": results
        }

    @staticmethod
    def clear():

        memory_store.clear()

        return {
            "success": True,
            "output": "memory cleared"
        }
