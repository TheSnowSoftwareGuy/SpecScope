from fastapi import Header, HTTPException
from ..config import settings

async def rate_limit(x_api_key: str | None = Header(default=None)):
    # Placeholder for rate limit. Can use IP-based or API key-based in prod.
    return
