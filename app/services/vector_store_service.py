import os
import json

import faiss
import numpy as np

from app.config import (
    FAISS_DIMENSION,
    FAISS_INDEX_PATH,
    FAISS_MAPPING_PATH,
    SIMILARITY_THRESHOLD,
)

from app.exceptions import VectorStoreException
from app.logger import logger


class VectorStoreService:
    """
    Persistent Singleton FAISS Vector Store.
    """

    _instance = None

    def __new__(cls, dimension: int = FAISS_DIMENSION):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            os.makedirs("data", exist_ok=True)

            cls._instance.dimension = dimension

            try:

                if os.path.exists(FAISS_INDEX_PATH):

                    cls._instance.index = faiss.read_index(
                        FAISS_INDEX_PATH
                    )

                    logger.info("Loaded FAISS index.")

                else:

                    cls._instance.index = faiss.IndexFlatIP(
                        dimension
                    )

                    logger.info("Created new FAISS index.")

                if os.path.exists(FAISS_MAPPING_PATH):

                    with open(
                        FAISS_MAPPING_PATH,
                        "r"
                    ) as f:

                        mapping = json.load(f)

                    cls._instance.id_to_cache_id = {
                        int(k): int(v)
                        for k, v in mapping.items()
                    }

                else:

                    cls._instance.id_to_cache_id = {}

                cls._instance.next_id = len(
                    cls._instance.id_to_cache_id
                )

            except Exception as e:

                raise VectorStoreException(
                    f"Failed initializing Vector Store: {e}"
                )

        return cls._instance

    # -----------------------------------------

    def add(
        self,
        cache_id: int,
        embedding: list[float]
    ):

        try:

            vector = np.array(
                embedding,
                dtype=np.float32
            ).reshape(1, -1)

            faiss.normalize_L2(vector)

            self.index.add(vector)

            self.id_to_cache_id[self.next_id] = cache_id

            self.next_id += 1

            self.save()

        except Exception as e:

            raise VectorStoreException(
                f"Failed adding vector: {e}"
            )

    # -----------------------------------------

    def search(
        self,
        embedding: list[float],
        threshold: float = SIMILARITY_THRESHOLD
    ):

        try:

            if self.index.ntotal == 0:
                return None

            query = np.array(
                embedding,
                dtype=np.float32
            ).reshape(1, -1)

            faiss.normalize_L2(query)

            scores, indices = self.index.search(query, 1)

            score = float(scores[0][0])

            index = int(indices[0][0])

            if index == -1:
                return None

            if score < threshold:
                return None

            return {
                "cache_id": self.id_to_cache_id[index],
                "score": score,
            }

        except Exception as e:

            raise VectorStoreException(
                f"Vector search failed: {e}"
            )

    # -----------------------------------------

    def save(self):

        try:

            faiss.write_index(
                self.index,
                FAISS_INDEX_PATH
            )

            with open(
                FAISS_MAPPING_PATH,
                "w"
            ) as f:

                json.dump(
                    self.id_to_cache_id,
                    f,
                    indent=4
                )

        except Exception as e:

            raise VectorStoreException(
                f"Failed saving FAISS index: {e}"
            )

    # -----------------------------------------

    def total_vectors(self):

        return self.index.ntotal