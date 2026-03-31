import random
import functools

def retry(max_attempts):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    print(f"[retry] Attempt {attempt} succeeded!")
                    return result
                except Exception as e:
                    last_exception = e
                    print(f"[retry] Attempt {attempt} failed: {e}")
            raise Exception(f"All {max_attempts} attempts failed") from last_exception
        return wrapper
    return decorator

random.seed(42)

@retry(max_attempts=5)
def fetch_data():
    """Simulates a flaky API call."""
    if random.choice([True, False]):
        raise ConnectionError("Server unreachable")
    return {"status": "ok", "data": [1, 2, 3]}

result = fetch_data()
print(f"Result: {result}")