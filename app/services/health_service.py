import os
import requests
import redis

from dotenv import load_dotenv

from app.services.vector_store_service import VectorStoreService

load_dotenv()


class HealthService:

    def __init__(self):

        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True,
        )

        self.vector_store = VectorStoreService()

        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def check(self):

        report = {"status": "healthy", "providers": {}}

        # ---------------------------------
        # Ollama
        # ---------------------------------

        try:

            response = requests.get(
                f"{self.ollama_url}/api/tags",
                timeout=5,
            )

            response.raise_for_status()

            report["providers"]["ollama"] = "healthy"

        except Exception:

            report["providers"]["ollama"] = "unhealthy"
            report["status"] = "degraded"

        # ---------------------------------
        # Redis / Memurai
        # ---------------------------------

        try:

            self.redis_client.ping()

            report["providers"]["redis"] = "healthy"

        except Exception:

            report["providers"]["redis"] = "unhealthy"
            report["status"] = "degraded"

        # ---------------------------------
        # FAISS
        # ---------------------------------

        try:

            report["providers"]["faiss"] = {
                "status": "healthy",
                "vectors": self.vector_store.total_vectors(),
            }

        except Exception:

            report["providers"]["faiss"] = "unhealthy"
            report["status"] = "degraded"

        return report
