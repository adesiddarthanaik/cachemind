"""
Application Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# Redis
# ==========================================================

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))

# ==========================================================
# Semantic Cache
# ==========================================================

SEMANTIC_CACHE_THRESHOLD = float(
    os.getenv(
        "SEMANTIC_CACHE_THRESHOLD",
        0.80,
    )
)

# ==========================================================
# Cache Eviction
# ==========================================================

MAX_CACHE_ENTRIES = int(
    os.getenv(
        "MAX_CACHE_ENTRIES",
        10000,
    )
)

EVICTION_POLICY = os.getenv(
    "EVICTION_POLICY",
    "lru",
).lower()

# ==========================================================
# Default LLM Settings
# ==========================================================

DEFAULT_MODEL = os.getenv(
    "DEFAULT_MODEL",
    "qwen2.5:3b",
)

DEFAULT_TEMPERATURE = float(
    os.getenv(
        "DEFAULT_TEMPERATURE",
        0.7,
    )
)

DEFAULT_MAX_TOKENS = int(
    os.getenv(
        "DEFAULT_MAX_TOKENS",
        512,
    )
)

# ==========================================================
# FAISS
# ==========================================================

FAISS_DIMENSION = int(
    os.getenv(
        "FAISS_DIMENSION",
        384,
    )
)

FAISS_INDEX_PATH = os.getenv(
    "FAISS_INDEX_PATH",
    "data/faiss.index",
)

FAISS_MAPPING_PATH = os.getenv(
    "FAISS_MAPPING_PATH",
    "data/faiss_mapping.json",
)

# ==========================================================
# Embeddings
# ==========================================================

EMBEDDING_PROVIDER = os.getenv(
    "EMBEDDING_PROVIDER",
    "minilm",
)

EMBEDDING_DIMENSION = int(
    os.getenv(
        "EMBEDDING_DIMENSION",
        384,
    )
)

# ==========================================================
# Ollama
# ==========================================================

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

# ==========================================================
# OpenRouter
# ==========================================================

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY",
    "",
)

OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1",
)

# ==========================================================
# Provider Fallback
# ==========================================================

FALLBACK_PROVIDER = os.getenv(
    "FALLBACK_PROVIDER",
    "openrouter",
)

FALLBACK_MODEL = os.getenv(
    "FALLBACK_MODEL",
    "openai/gpt-4.1-mini",
)