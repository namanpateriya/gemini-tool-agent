import faiss
import numpy as np

from app.memory.embeddings import (
    embed_texts
)

from app.config import (
    TOP_K,
    MEMORY_LIMIT
)

from app.utils.logger import get_logger

logger = get_logger(__name__)


class VectorMemoryStore:

    def __init__(self):

        self.index = None
        self.memories = []

    def add_memory(self, text: str):

        if not text or not text.strip():
            return

        embedding = embed_texts([text])

        embedding = np.array(
            embedding
        ).astype("float32")

        if self.index is None:

            dimension = embedding.shape[1]

            self.index = faiss.IndexFlatL2(
                dimension
            )

        self.index.add(embedding)

        self.memories.append(text)

        if len(self.memories) > MEMORY_LIMIT:

            self.memories = (
                self.memories[-MEMORY_LIMIT:]
            )

        logger.info(
            f"Memory added. Count={len(self.memories)}"
        )

    def search(self, query: str):

        if (
            self.index is None
            or not self.memories
        ):
            return []

        query_embedding = embed_texts([query])

        query_embedding = np.array(
            query_embedding
        ).astype("float32")

        top_k = min(
            TOP_K,
            len(self.memories)
        )

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for idx in indices[0]:

            if 0 <= idx < len(self.memories):

                results.append(
                    self.memories[idx]
                )

        return results

    def clear(self):

        self.index = None
        self.memories = []

        logger.info(
            "Memory cleared"
        )
