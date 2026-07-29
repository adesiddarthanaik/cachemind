from sentence_transformers import SentenceTransformer
from app.embeddings.embedding_service import EmbeddingProvider
from app.logger import logger


class MiniLMEmbeddingProvider(EmbeddingProvider):

    def __init__(self):
        self.model = None

    def _get_model(self):

        if self.model is None:
            logger.info("STEP 1: About to load MiniLM model")

            self.model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )

            logger.info("STEP 2: MiniLM model loaded")

        return self.model

    def generate_embedding(self, text: str) -> list[float]:

        logger.info("STEP 3: generate_embedding() entered")

        model = self._get_model()

        logger.info("STEP 4: Starting model.encode()")

        embedding = model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        logger.info("STEP 5: model.encode() completed")

        return embedding.tolist()