import time
from threading import Lock


class MetricsService:
    """
    Singleton Metrics Service.

    Tracks runtime statistics for CacheMind.
    """

    _instance = None
    _lock = Lock()

    def __new__(cls):

        if cls._instance is None:

            with cls._lock:

                if cls._instance is None:

                    cls._instance = super().__new__(cls)

                    cls._instance.started_at = time.time()

                    cls._instance.total_requests = 0

                    cls._instance.cache_hits = 0

                    cls._instance.cache_misses = 0

                    cls._instance.provider_calls = 0

                    cls._instance.total_similarity = 0.0

                    cls._instance.total_request_time = 0.0

                    cls._instance.total_cache_time = 0.0

                    cls._instance.total_provider_time = 0.0

                    cls._instance.tokens_saved = 0

        return cls._instance

    # --------------------------------------------------
    # Request Metrics
    # --------------------------------------------------

    def request(self):

        self.total_requests += 1

    def request_time(self, seconds: float):

        self.total_request_time += seconds

    # --------------------------------------------------
    # Cache Metrics
    # --------------------------------------------------

    def cache_hit(self, similarity: float):

        self.cache_hits += 1

        self.total_similarity += similarity

    def cache_miss(self):

        self.cache_misses += 1

    def cache_time(self, seconds: float):

        self.total_cache_time += seconds

    # --------------------------------------------------
    # Provider Metrics
    # --------------------------------------------------

    def provider_call(self):

        self.provider_calls += 1

    def provider_time(self, seconds: float):

        self.total_provider_time += seconds

    # --------------------------------------------------
    # Token Savings
    # --------------------------------------------------

    def save_tokens(self, text: str):

        estimated_tokens = int(
            len(text.split()) * 1.3
        )

        self.tokens_saved += estimated_tokens

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def reset(self):

        self.started_at = time.time()

        self.total_requests = 0

        self.cache_hits = 0

        self.cache_misses = 0

        self.provider_calls = 0

        self.total_similarity = 0.0

        self.total_request_time = 0.0

        self.total_cache_time = 0.0

        self.total_provider_time = 0.0

        self.tokens_saved = 0

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    def stats(self):

        cache_hit_rate = 0

        if self.total_requests:

            cache_hit_rate = (
                self.cache_hits
                / self.total_requests
            ) * 100

        average_similarity = 0

        if self.cache_hits:

            average_similarity = (
                self.total_similarity
                / self.cache_hits
            )

        average_request_time = 0

        if self.total_requests:

            average_request_time = (
                self.total_request_time
                / self.total_requests
            )

        average_cache_time = 0

        if self.cache_hits:

            average_cache_time = (
                self.total_cache_time
                / self.cache_hits
            )

        average_provider_time = 0

        if self.provider_calls:

            average_provider_time = (
                self.total_provider_time
                / self.provider_calls
            )

        uptime = round(
            time.time() - self.started_at,
            2
        )

        estimated_cost = round(
            (self.tokens_saved / 1_000_000) * 0.15,
            6,
        )

        return {

            "total_requests": self.total_requests,

            "cache_hits": self.cache_hits,

            "cache_misses": self.cache_misses,

            "provider_calls": self.provider_calls,

            "cache_hit_rate": round(
                cache_hit_rate,
                2,
            ),

            "average_similarity": round(
                average_similarity,
                4,
            ),

            "average_request_time_ms": round(
                average_request_time * 1000,
                2,
            ),

            "average_cache_time_ms": round(
                average_cache_time * 1000,
                2,
            ),

            "average_provider_time_ms": round(
                average_provider_time * 1000,
                2,
            ),

            "uptime_seconds": uptime,

            "estimated_tokens_saved": self.tokens_saved,

            "estimated_cost_saved_usd": estimated_cost,
        }