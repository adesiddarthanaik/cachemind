from prometheus_client import Counter, Histogram

# Total API requests
REQUEST_COUNTER = Counter(
    "cachemind_requests_total",
    "Total number of API requests",
)

# Semantic cache hits
CACHE_HIT_COUNTER = Counter(
    "cachemind_cache_hits_total",
    "Total number of semantic cache hits",
)

# Semantic cache misses
CACHE_MISS_COUNTER = Counter(
    "cachemind_cache_misses_total",
    "Total number of semantic cache misses",
)

# Provider calls
PROVIDER_REQUEST_COUNTER = Counter(
    "cachemind_provider_requests_total",
    "Total number of provider API requests",
)

# Total request latency
REQUEST_LATENCY = Histogram(
    "cachemind_request_duration_seconds",
    "Request processing time",
)

# Provider latency
PROVIDER_LATENCY = Histogram(
    "cachemind_provider_duration_seconds",
    "Provider response time",
)
