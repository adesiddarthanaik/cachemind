from sentence_transformers import SentenceTransformer
from app.embeddings.embedding_service import EmbeddingProvider


class MiniLMEmbeddingProvider(EmbeddingProvider):
    """
    Local embedding provider using Sentence Transformers.
    """

    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def generate_embedding(self, text: str) -> list[float]:
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embedding.tolist()