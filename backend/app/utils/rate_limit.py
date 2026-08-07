from slowapi import Limiter
from slowapi.util import get_remote_address
import os

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

def rate_limit(limit_per_minute: int):
    """Return a decorator that applies the limit, or bypasses in test mode."""
    def decorator(func):
        if os.getenv("TEST_MODE", "false").lower() == "true":
            return func  # Skip rate limiting entirely
        return limiter.limit(f"{limit_per_minute}/minute")(func)
    return decorator