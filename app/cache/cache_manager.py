import redis
from datetime import datetime, timedelta

from app.exceptions import CacheException
from app.config import (
    REDIS_HOST,
    REDIS_PORT,
    CACHE_TTL,
    MAX_CACHE_ENTRIES,
    EVICTION_POLICY,
)

from app.models.cache_entry import CacheEntry
from app.services.eviction_policy_service import EvictionPolicyService
from app.logger import logger


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

    # -----------------------------------------

    def _update_entry(self, entry: "CacheEntry"):

        self.client.set(
            f"cache:{entry.id}",
            entry.model_dump_json(),
            ex=entry.ttl
        )

    # -----------------------------------------

    def _evict_if_needed(self):

        current_size = self.count()

        if current_size < MAX_CACHE_ENTRIES:
            return

        entries = self.get_all_entries()

        victim = EvictionPolicyService.select_victim(
            entries,
            EVICTION_POLICY,
        )

        if victim:

            logger.info(
                f"Evicting cache entry {victim.id}"
            )

            self.delete(victim.id)

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

            now = datetime.now()

            self._evict_if_needed()

            entry = CacheEntry(
                id=cache_id,
                prompt=prompt,
                response=response,
                model=model,
                system_prompt_hash=system_prompt_hash,
                temperature=temperature,
                max_tokens=max_tokens,
                timestamp=now,
                ttl=ttl,
                created_at=now,
                last_accessed=now,
                expires_at=now + timedelta(seconds=ttl),
                access_count=1,
            )

            self._update_entry(entry)

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

            if datetime.now() > entry.expires_at:

                self.delete(cache_id)
                return None

            entry.last_accessed = datetime.now()
            entry.access_count += 1
            entry.hit_count += 1

            self._update_entry(entry)

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

    # -----------------------------------------

    def count(self) -> int:
        """
        Returns the total number of cache entries.
        """

        try:

            return len(
                self.client.keys("cache:*")
            )

        except Exception as e:

            raise CacheException(
                f"Failed to count cache entries: {e}"
            )

    # -----------------------------------------

    def get_all_entries(self):
        """
        Returns all cache entries.
        """

        try:

            entries = []

            for key in self.client.keys("cache:*"):

                data = self.client.get(key)

                if data:

                    entries.append(
                        CacheEntry.model_validate_json(data)
                    )

            return entries

        except Exception as e:

            raise CacheException(
                f"Failed to retrieve cache entries: {e}"
            )

    # -----------------------------------------

    def save_entry(self, entry: CacheEntry):
        """
        Saves an updated CacheEntry.
        """

        self._update_entry(entry)