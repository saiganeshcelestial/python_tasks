import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timer] {func.__name__} executed in {elapsed:.4f}s")
        return result
    return wrapper

@timer
def compute_squares(n):
    """Computes sum of squares from 1 to n."""
    return sum(i * i for i in range(1, n + 1))

result = compute_squares(1_000_000)
print(f"Result: {result}")
print(f"Function name: {compute_squares.__name__}")
print(f"Docstring: {compute_squares.__doc__}")