import redis
from datetime import datetime

from app.exceptions import CacheException
from app.config import (
    REDIS_HOST,
    REDIS_PORT,
    CACHE_TTL,
)

from app.models.cache_entry import CacheEntry


class CacheManager:
    """
    Handles all Redis cache operations.
    """

    def __init__(self):

        try:

            self.client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                decode_responses=True
            )

        except Exception as e:

            raise CacheException(
                f"Failed to connect to Redis: {e}"
            )

    # -----------------------------------------

    def set(
        self,
        cache_id: int,
        prompt: str,
        response: str,
        model: str,
        system_prompt_hash: str,
        temperature: float,
        max_tokens: int,
        ttl: int = CACHE_TTL
    ):

        try:

            entry = CacheEntry(
                id=cache_id,
                prompt=prompt,
                response=response,
                model=model,
                system_prompt_hash=system_prompt_hash,
                temperature=temperature,
                max_tokens=max_tokens,
                timestamp=datetime.utcnow(),
                ttl=ttl
            )

            self.client.set(
                f"cache:{cache_id}",
                entry.model_dump_json(),
                ex=ttl
            )

        except Exception as e:

            raise CacheException(
                f"Failed to store cache entry: {e}"
            )

    # -----------------------------------------

    def get(self, cache_id: int):

        try:

            data = self.client.get(
                f"cache:{cache_id}"
            )

            if data is None:
                return None

            entry = CacheEntry.model_validate_json(data)

            entry.hit_count += 1

            self.client.set(
                f"cache:{cache_id}",
                entry.model_dump_json(),
                ex=entry.ttl
            )

            return entry

        except Exception as e:

            raise CacheException(
                f"Failed to retrieve cache entry: {e}"
            )

    # -----------------------------------------

    def delete(self, cache_id: int):

        try:

            self.client.delete(
                f"cache:{cache_id}"
            )

        except Exception as e:

            raise CacheException(
                f"Failed to delete cache entry: {e}"
            )

    # -----------------------------------------

    def exists(self, cache_id: int):

        try:

            return self.client.exists(
                f"cache:{cache_id}"
            )

        except Exception as e:

            raise CacheException(
                f"Failed to check cache entry: {e}"
            )