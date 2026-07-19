from datetime import datetime
from typing import List, Optional

from app.models.cache_entry import CacheEntry


class EvictionPolicyService:
    """
    Determines which cache entry should be evicted.

    Supported policies:
        - LRU (Least Recently Used)
        - LFU (Least Frequently Used)
        - TTL (Expired Entries)
    """

    @staticmethod
    def lru(entries: List[CacheEntry]) -> Optional[CacheEntry]:
        """
        Returns the least recently used cache entry.
        """

        if not entries:
            return None

        return min(
            entries,
            key=lambda entry: entry.last_accessed
        )

    @staticmethod
    def lfu(entries: List[CacheEntry]) -> Optional[CacheEntry]:
        """
        Returns the least frequently used cache entry.
        """

        if not entries:
            return None

        return min(
            entries,
            key=lambda entry: entry.access_count
        )

    @staticmethod
    def ttl(entries: List[CacheEntry]) -> Optional[CacheEntry]:
        """
        Returns the first expired cache entry.
        """

        now = datetime.now()

        expired = [
            entry
            for entry in entries
            if entry.expires_at <= now
        ]

        if not expired:
            return None

        return min(
            expired,
            key=lambda entry: entry.expires_at
        )

    @staticmethod
    def select_victim(
        entries: List[CacheEntry],
        policy: str,
    ) -> Optional[CacheEntry]:
        """
        Selects a cache entry according to the configured eviction policy.
        """

        policy = policy.lower()

        if policy == "lru":
            return EvictionPolicyService.lru(entries)

        if policy == "lfu":
            return EvictionPolicyService.lfu(entries)

        if policy == "ttl":
            return EvictionPolicyService.ttl(entries)

        raise ValueError(
            f"Unsupported eviction policy: {policy}"
        )
