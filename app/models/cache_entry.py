from datetime import datetime, timedelta
from pydantic import BaseModel, Field


class CacheEntry(BaseModel):
    """
    Represents one cached LLM response.
    """

    # ----------------------------
    # Cache Identity
    # ----------------------------

    id: int

    prompt: str

    response: str

    # ----------------------------
    # LLM Metadata
    # ----------------------------

    model: str

    system_prompt_hash: str

    temperature: float

    max_tokens: int

    # ----------------------------
    # Time Metadata
    # ----------------------------

    timestamp: datetime = Field(default_factory=datetime.now)

    created_at: datetime = Field(default_factory=datetime.now)

    last_accessed: datetime = Field(default_factory=datetime.now)

    expires_at: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(hours=1)
    )

    # ----------------------------
    # Usage Metadata
    # ----------------------------

    hit_count: int = 0

    access_count: int = 0

    # ----------------------------
    # TTL
    # ----------------------------

    ttl: int = 3600