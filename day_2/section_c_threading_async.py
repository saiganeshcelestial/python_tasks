# ============================================================
# Day-2 | Section C — Threading, Multiprocessing & Async
# ============================================================
import time
import threading
import multiprocessing
import asyncio
from datetime import datetime


# ─────────────────────────────────────────────────────────────
# Q8. Thread vs Sequential — IO Simulation
# ─────────────────────────────────────────────────────────────
def fetch_data(source, delay):
    print(f"  [{datetime.now().strftime('%H:%M:%S')}] START  {source}")
    time.sleep(delay)
    print(f"  [{datetime.now().strftime('%H:%M:%S')}] DONE   {source}")


sources = [("users", 2), ("orders", 3), ("products", 1), ("reviews", 2), ("inventory", 1)]

print("--- Q8: Sequential ---")
start = time.time()
for source, delay in sources:
    fetch_data(source, delay)
print(f"Sequential time: {time.time() - start:.1f}s\n")

print("--- Q8: Threaded ---")
start = time.time()
threads = [threading.Thread(target=fetch_data, args=(s, d)) for s, d in sources]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"Threaded time: {time.time() - start:.1f}s\n")


# ─────────────────────────────────────────────────────────────
# Q9. Race Condition — Shared Counter Fix
# ─────────────────────────────────────────────────────────────
def increment_unsafe(container):
    for _ in range(1000):
        container[0] += 1

def increment_safe(container, lock):
    for _ in range(1000):
        with lock:
            container[0] += 1

print("--- Q9: Without Lock ---")
counter = [0]
threads = [threading.Thread(target=increment_unsafe, args=(counter,)) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"Without lock: {counter[0]} (expected 10000, often wrong)")

print("--- Q9: With Lock ---")
counter = [0]
lock = threading.Lock()
threads = [threading.Thread(target=increment_safe, args=(counter, lock)) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"With lock:    {counter[0]} (always 10000)\n")


# ─────────────────────────────────────────────────────────────
# Q10. Multiprocessing — CPU-bound Speedup
# ─────────────────────────────────────────────────────────────
def compute_squares(n):
    return sum(i * i for i in range(1, n + 1))

values = [10_000_000, 20_000_000, 15_000_000, 25_000_000]

print("--- Q10: Sequential ---")
start = time.time()
results = [compute_squares(n) for n in values]
seq_time = time.time() - start
for v, r in zip(values, results):
    print(f"  compute_squares({v:,}) = {r}")
print(f"Sequential time: {seq_time:.2f}s\n")

print("--- Q10: Multiprocessing ---")
start = time.time()
with multiprocessing.Pool() as pool:
    results = pool.map(compute_squares, values)
mp_time = time.time() - start
for v, r in zip(values, results):
    print(f"  compute_squares({v:,}) = {r}")
print(f"Multiprocessing time: {mp_time:.2f}s (speedup: {seq_time/mp_time:.1f}x)\n")


# ─────────────────────────────────────────────────────────────
# Q11. Async IO — Concurrent API Simulation
# ─────────────────────────────────────────────────────────────
async def fetch(url, delay):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"  [{ts}] START  {url}")
    await asyncio.sleep(delay)
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"  [{ts}] DONE   {url}")
    return url

urls = [("api/users", 2), ("api/orders", 3), ("api/products", 1), ("api/reviews", 2)]

def sync_version():
    for url, delay in urls:
        time.sleep(delay)

print("--- Q11: Sync ---")
start = time.time()
sync_version()
print(f"Sync time:  {time.time() - start:.1f}s\n")

async def async_version():
    tasks = [fetch(url, delay) for url, delay in urls]
    await asyncio.gather(*tasks)

print("--- Q11: Async ---")
start = time.time()
asyncio.run(async_version())
print(f"Async time: {time.time() - start:.1f}s\n")
