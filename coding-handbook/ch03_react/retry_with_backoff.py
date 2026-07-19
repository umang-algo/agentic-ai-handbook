"""
Chapter 3: Exponential Backoff with Full Jitter
=================================================
Production retry logic for handling rate limits (HTTP 429) and transient
network errors. Uses full jitter to prevent synchronized retry storms.

From: The Practitioner's Handbook of Agentic AI, Chapter 3.5
"""

import time
import random
import logging
from typing import Callable, TypeVar

T = TypeVar('T')
logger = logging.getLogger(__name__)


def with_backoff(fn: Callable[[], T],
                 max_retries: int = 6,
                 base_delay: float = 1.0,
                 max_delay: float = 60.0) -> T:
    """
    Full-jitter exponential backoff.
    Expected wait on attempt k: base_delay * 2^k * Uniform(0,1)
    """
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries:
                raise
            # Full jitter: random between 0 and cap
            cap = min(max_delay, base_delay * (2 ** attempt))
            sleep = random.uniform(0, cap)
            logger.warning(
                f"Attempt {attempt+1} failed: {e}. "
                f"Retrying in {sleep:.1f}s"
            )
            time.sleep(sleep)


# ─── Demo ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(message)s")

    print("=" * 55)
    print("Exponential Backoff with Full Jitter Demo")
    print("=" * 55)

    call_count = 0

    def flaky_api_call():
        """Simulates an API that fails 3 times then succeeds."""
        global call_count
        call_count += 1
        if call_count < 4:
            raise ConnectionError(f"Rate limited (attempt {call_count})")
        return {"status": "success", "data": "Hello from API"}

    result = with_backoff(flaky_api_call, max_retries=5, base_delay=0.1)
    print(f"\n✅ Result after {call_count} attempts: {result}")
