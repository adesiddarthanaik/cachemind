from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    """
    Centralized application configuration.
    """

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")

    # Redis
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    # Cache
    CACHE_SIMILARITY_THRESHOLD = float(os.getenv("CACHE_SIMILARITY_THRESHOLD", 0.95))

    CACHE_TTL = int(os.getenv("CACHE_TTL", 86400))


settings = Settings()
