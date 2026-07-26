from openai import OpenAI
from app.config.settings import settings
from app.embeddings.embedding_service import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """
    OpenAI implementation of the EmbeddingProvider interface.
    """

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_embedding(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=settings.EMBEDDING_MODEL, input=text
        )

        return response.data[0].embedding
