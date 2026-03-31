import functools
import time


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retries the wrapped function up to max_attempts times on exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    print(f"[RETRY] Attempt {attempt}/{max_attempts} failed for {func.__name__}: {exc}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator
