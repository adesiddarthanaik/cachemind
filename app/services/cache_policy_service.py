from app.logger import logger


class CachePolicyService:
    """
    Determines whether a semantic cache entry should be used.
    """

    DEFAULT_THRESHOLD = 0.95

    def __init__(self, threshold: float = DEFAULT_THRESHOLD):

        self.threshold = threshold

    def should_use_cache(
        self,
        similarity: float,
        cached_entry,
        model: str,
        system_prompt_hash: str,
        temperature: float,
        max_tokens: int,
    ) -> bool:

        # Similarity threshold
        if similarity < self.threshold:

            logger.info(f"Cache rejected (similarity={similarity:.4f})")

            return False

        # Model mismatch
        if cached_entry.model != model:

            logger.info("Cache rejected (model mismatch)")

            return False

        # System Prompt mismatch
        if cached_entry.system_prompt_hash != system_prompt_hash:

            logger.info("Cache rejected (system prompt mismatch)")

            return False

        # Temperature mismatch
        if cached_entry.temperature != temperature:

            logger.info("Cache rejected (temperature mismatch)")

            return False

        # Max Tokens mismatch
        if cached_entry.max_tokens != max_tokens:

            logger.info("Cache rejected (max_tokens mismatch)")

            return False

        logger.info("Cache accepted by Policy Engine.")

        return True
