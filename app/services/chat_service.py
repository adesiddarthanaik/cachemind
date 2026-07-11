from app.cache.cache_manager import CacheManager
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
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

    Flow:
    User Request
            ↓
    Generate Embedding
            ↓
    Semantic Search (FAISS)
            ↓
      Cache Hit / Miss
            ↓
    Provider (if needed)
            ↓
    Store in Redis + FAISS
            ↓
    Return Response
    """

    def __init__(self):

        self.cache = CacheManager()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

    def ask(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: str,
    ):

        logger.info("ChatService called")

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

        try:

            logger.info(
                f"Total vectors: {self.vector_store.total_vectors()}"
            )

            result = self.vector_store.search(embedding)

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

                if (
                    entry.system_prompt_hash == system_prompt_hash
                    and entry.model == model
                    and entry.temperature == temperature
                    and entry.max_tokens == max_tokens
                ):

                    logger.info(
                        f"Semantic Cache HIT "
                        f"(Similarity={result['score']:.4f})"
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

        # ---------------------------------
        # Provider Call
        # ---------------------------------

        try:

            logger.info(
                f"Calling ProviderFactory ({model})"
            )

            provider = ProviderFactory.get_provider(model)

            answer = provider.generate(
                prompt=prompt,
                model=model,
            )

        except ProviderException:

            logger.exception("Provider selection failed.")

            raise

        except Exception:

            logger.exception("Provider request failed.")

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

        return {
            "source": "provider",
            "response": answer,
        }