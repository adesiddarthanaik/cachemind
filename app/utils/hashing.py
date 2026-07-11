import hashlib


def hash_text(text: str) -> str:
    """
    Returns a SHA256 hash of any text.
    """

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()