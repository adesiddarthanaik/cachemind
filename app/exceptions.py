class CacheMindException(Exception):
    """Base exception for CacheMind."""


class ProviderException(CacheMindException):
    """Raised when an LLM provider fails."""


class EmbeddingException(CacheMindException):
    """Raised when embedding generation fails."""


class CacheException(CacheMindException):
    """Raised when Redis operations fail."""


class VectorStoreException(CacheMindException):
    """Raised when FAISS operations fail."""
