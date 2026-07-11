"""
Application Configuration
"""

# -----------------------------
# Redis
# -----------------------------

REDIS_HOST = "localhost"
REDIS_PORT = 6379
CACHE_TTL = 3600

# -----------------------------
# Semantic Cache
# -----------------------------

SIMILARITY_THRESHOLD = 0.80

# -----------------------------
# Default LLM Settings
# -----------------------------

DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 512

# -----------------------------
# FAISS
# -----------------------------

FAISS_DIMENSION = 384
FAISS_INDEX_PATH = "data/faiss.index"
FAISS_MAPPING_PATH = "data/faiss_mapping.json"

# -----------------------------
# Embeddings
# -----------------------------

EMBEDDING_PROVIDER = "minilm"
EMBEDDING_DIMENSION = 384