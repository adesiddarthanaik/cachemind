import time

from app.cache.cache_manager import CacheManager
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.services.cache_policy_service import CachePolicyService
from app.services.metrics_service import MetricsService
from app.metrics.prometheus import (
    REQUEST_COUNTER,
    CACHE_HIT_COUNTER,
    CACHE_MISS_COUNTER,
    PROVIDER_REQUEST_COUNTER,
    REQUEST_LATENCY,
    PROVIDER_LATENCY,
)
from app.providers.provider_factory import ProviderFactory
from app.utils.hashing import hash_text
from app.logger import logger

from app.exceptions import (
    EmbeddingException,
    CacheException,
    VectorStoreException,
    ProviderException,
)


class ChatService:
    """
    Main orchestration service for CacheMind.
    """

    def __init__(self):

        self.cache = CacheManager()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()
        self.policy = CachePolicyService()
        self.metrics = MetricsService()

    # ---------------------------------
    # Stream Cached Response
    # ---------------------------------

    def _stream_cached_response(self, text: str):

        words = text.split()

        for word in words:
            yield word + " "

    def ask(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: str,
        stream: bool = False,
    ):

        logger.info("ChatService called")

        start_time = time.perf_counter()

        self.metrics.request()
        REQUEST_COUNTER.inc()

        # ---------------------------------
        # Generate Metadata
        # ---------------------------------

        system_prompt_hash = hash_text(system_prompt)

        # ---------------------------------
        # Generate Embedding
        # ---------------------------------

        try:

            embedding = self.embedding_service.generate(prompt)

            logger.info("Embedding generated")

        except EmbeddingException:

            logger.exception("Embedding generation failed.")
            raise

        except Exception:

            logger.exception("Unexpected embedding error.")
            raise

        # ---------------------------------
        # Semantic Search
        # ---------------------------------

        cache_start = time.perf_counter()

        try:

            logger.info(
                f"Total vectors: {self.vector_store.total_vectors()}"
            )

            result = self.vector_store.search(embedding)

            cache_elapsed = time.perf_counter() - cache_start

            logger.info(
                f"FAISS Search Result: {result}"
            )

        except VectorStoreException:

            logger.exception("Vector Store search failed.")
            raise

        except Exception:

            logger.exception("Unexpected FAISS error.")
            raise

        # ---------------------------------
        # Cache Lookup
        # ---------------------------------

        if result:

            try:

                entry = self.cache.get(result["cache_id"])

            except CacheException:

                logger.exception("Redis lookup failed.")
                raise

            logger.info(f"Redis Entry: {entry}")

            if entry:

                if self.policy.should_use_cache(
                    similarity=result["score"],
                    cached_entry=entry,
                    model=model,
                    system_prompt_hash=system_prompt_hash,
                    temperature=temperature,
                    max_tokens=max_tokens,
                ):

                    logger.info(
                        f"Semantic Cache HIT (Similarity={result['score']:.4f})"
                    )

                    self.metrics.cache_hit(
                        result["score"]
                    )
                    CACHE_HIT_COUNTER.inc()

                    self.metrics.cache_time(cache_elapsed)

                    self.metrics.save_tokens(
                        entry.response
                    )

                    # ---------------------------------
                    # Stream Cached Response
                    # ---------------------------------

                    if stream:

                        logger.info(
                            "Streaming cached response."
                        )

                        elapsed = (
                            time.perf_counter()
                            - start_time
                        )

                        self.metrics.request_time(
                            elapsed
                        )
                        REQUEST_LATENCY.observe(elapsed)

                        logger.info(
                            f"Request Latency: {elapsed*1000:.2f} ms"
                        )

                        return self._stream_cached_response(
                            entry.response
                        )

                    elapsed = (
                        time.perf_counter()
                        - start_time
                    )

                    self.metrics.request_time(
                        elapsed
                    )
                    REQUEST_LATENCY.observe(elapsed)

                    logger.info(
                        f"Request Latency: {elapsed*1000:.2f} ms"
                    )

                    logger.info(
                        f"Cache Latency: {cache_elapsed*1000:.2f} ms"
                    )

                    return {
                        "source": "semantic-cache",
                        "similarity": round(result["score"], 4),
                        "response": entry.response,
                    }

                logger.warning(
                    "Metadata mismatch. Ignoring cached response."
                )

            else:

                logger.warning(
                    "Redis cache entry not found."
                )

        else:

            logger.info("Semantic Cache MISS.")

            self.metrics.cache_miss()
            CACHE_MISS_COUNTER.inc()

        # ---------------------------------
        # Provider Call
        # ---------------------------------

        try:

            logger.info(
                f"Calling ProviderFactory ({model})"
            )

            logger.info(
                f"Requested Model: {model}"
            )

            provider = ProviderFactory.get_provider(model)

            logger.info(
                f"Selected Provider: {provider.__class__.__name__}"
            )

            try:

                self.metrics.provider_call()
                PROVIDER_REQUEST_COUNTER.inc()

                provider_start = time.perf_counter()

                answer = provider.generate(
                    prompt=prompt,
                    model=model,
                    stream=stream,
                )

                provider_elapsed = (
                    time.perf_counter()
                    - provider_start
                )

                self.metrics.provider_time(
                    provider_elapsed
                )

                logger.info(
                    "Primary provider response received."
                )

            except Exception as primary_error:

                logger.warning(
                    f"Primary provider failed: {primary_error}"
                )

                logger.info(
                    "Attempting OpenRouter fallback..."
                )

                from app.providers.openrouter_provider import OpenRouterProvider

                fallback_provider = OpenRouterProvider()

                answer = fallback_provider.generate(
                    prompt=prompt,
                    model="openai/gpt-4.1-mini",
                    stream=False,
                )

                logger.info(
                    "Fallback provider response received."
                )

            # ---------------------------------
            # Stream Provider Response
            # ---------------------------------

            if stream:

                logger.info(
                    "Streaming provider response."
                )

                elapsed = (
                    time.perf_counter()
                    - start_time
                )

                self.metrics.request_time(
                    elapsed
                )
                REQUEST_LATENCY.observe(elapsed)

                logger.info(
                    f"Request Latency: {elapsed*1000:.2f} ms"
                )

                return answer

        except ProviderException:

            logger.exception(
                "Provider selection failed."
            )
            raise

        except Exception:

            logger.exception(
                "Provider request failed."
            )
            raise

        # ---------------------------------
        # Store Cache
        # ---------------------------------

        cache_id = self.vector_store.next_id

        logger.info(
            f"Saving Cache ID: {cache_id}"
        )

        try:

            self.cache.set(
                cache_id=cache_id,
                prompt=prompt,
                response=answer,
                model=model,
                system_prompt_hash=system_prompt_hash,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            self.vector_store.add(
                cache_id=cache_id,
                embedding=embedding,
            )

            logger.info(
                "Response stored in Redis and FAISS."
            )

        except (CacheException, VectorStoreException):

            logger.exception(
                "Failed to store response."
            )

            raise

        # ---------------------------------
        # Return Provider Response
        # ---------------------------------

        elapsed = (
            time.perf_counter()
            - start_time
        )

        self.metrics.request_time(
            elapsed
        )
        REQUEST_LATENCY.observe(elapsed)

        PROVIDER_LATENCY.observe(provider_elapsed)

        logger.info(
            f"Request Latency: {elapsed*1000:.2f} ms"
        )

        logger.info(
            f"Provider Latency: {provider_elapsed*1000:.2f} ms"
        )

        return {
            "source": "provider",
            "response": answer,
        }