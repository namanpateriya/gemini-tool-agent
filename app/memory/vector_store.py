import json
from pathlib import Path

import faiss
import numpy as np

from app.memory.embeddings import (
    embed_texts
)

from app.config import (
    TOP_K,
    MEMORY_LIMIT,
    MEMORY_SIMILARITY_THRESHOLD
)

from app.utils.logger import (
    get_logger
)

logger = get_logger(__name__)

MEMORY_FILE = (
    Path("data/memory_store.json")
)


class VectorMemoryStore:

    def __init__(self):

        self.index = None

        self.memories = []

        self.load_memories()

    def rebuild_index(self):

        if not self.memories:

            self.index = None

            return

        embeddings = embed_texts(
            self.memories
        )

        embeddings = np.array(
            embeddings
        ).astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.index.add(embeddings)

    def persist_memories(self):

        MEMORY_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.memories,
                f,
                indent=2
            )

    def load_memories(self):

        if not MEMORY_FILE.exists():

            return

        try:

            with open(
                MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                self.memories = json.load(f)

            self.rebuild_index()

            logger.info(
                "Persistent memory loaded"
            )

        except Exception as e:

            logger.error(
                f"Memory load failed: {e}"
            )

    def add_memory(
        self,
        text: str
    ):

        if not text.strip():

            return

        self.memories.append(text)

        if len(self.memories) > MEMORY_LIMIT:

            self.memories = (
                self.memories[-MEMORY_LIMIT:]
            )

        self.rebuild_index()

        self.persist_memories()

        logger.info(
            f"Memory added. "
            f"Count={len(self.memories)}"
        )

    def search(
        self,
        query: str
    ):

        if (
            self.index is None
            or not self.memories
        ):

            return []

        query_embedding = (
            embed_texts([query])
        )

        query_embedding = np.array(
            query_embedding
        ).astype("float32")

        top_k = min(
            TOP_K,
            len(self.memories)
        )

        distances, indices = (
            self.index.search(
                query_embedding,
                top_k
            )
        )

        results = []

        for idx, distance in zip(
            indices[0],
            distances[0]
        ):

            if (
                0 <= idx < len(self.memories)
                and distance
                <= MEMORY_SIMILARITY_THRESHOLD
            ):

                results.append(
                    self.memories[idx]
                )

        return results

    def clear(self):

        self.index = None

        self.memories = []

        self.persist_memories()

        logger.info(
            "Memory cleared"
        )
