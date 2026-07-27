from sentence_transformers import SentenceTransformer
from app.embeddings.embedding_service import EmbeddingProvider


class MiniLMEmbeddingProvider(EmbeddingProvider):
    """
    Local embedding provider using Sentence Transformers.
    """

    def __init__(self):
        # Do NOT load the model during startup.
        self.model = None

    def _get_model(self):
        """
        Lazily load the model on first use.
        """
        if self.model is None:
            print("Loading MiniLM model...")
            self.model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )

        return self.model

    def generate_embedding(self, text: str) -> list[float]:
        model = self._get_model()

        embedding = model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.tolist()