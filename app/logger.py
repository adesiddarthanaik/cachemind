import logging

from app.middleware.context import request_id_context


class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_context.get()
        return True


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | %(levelname)s | %(name)s | "
        "[%(request_id)s] | %(message)s"
    ),
)

# IMPORTANT:
# Attach the filter to every handler created by basicConfig.
root_logger = logging.getLogger()

for handler in root_logger.handlers:
    handler.addFilter(RequestIDFilter())

logger = logging.getLogger("CacheMind")