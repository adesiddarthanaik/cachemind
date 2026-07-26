from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import CACHEMIND_API_KEY
from app.rate_limit.limiter import rate_limiter


security = HTTPBearer(auto_error=False)


def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """
    Verify the API Key supplied in the Authorization header.

    Expected Header:

        Authorization: Bearer cm_xxxxxxxxxxxxxxxxxxxxx
    """

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header.",
        )

    token = credentials.credentials

    if token != CACHEMIND_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key.",
        )

    # Apply rate limiting per API key
    rate_limiter.check(token)

    return token