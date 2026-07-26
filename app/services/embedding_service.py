from app.embeddings.minilm_embedding_provider import MiniLMEmbeddingProvider
from app.exceptions import EmbeddingException
from app.config import EMBEDDING_PROVIDER


class EmbeddingService:
    """
    Service responsible for generating embeddings.
    """

    def __init__(self):

        if EMBEDDING_PROVIDER == "minilm":

            self.provider = MiniLMEmbeddingProvider()

        else:

            raise EmbeddingException(
                f"Unsupported embedding provider: {EMBEDDING_PROVIDER}"
            )

    def generate(self, text: str) -> list[float]:

        try:

            return self.provider.generate_embedding(text)

        except Exception as e:

            raise EmbeddingException(str(e))
