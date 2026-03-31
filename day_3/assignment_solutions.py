"""
Day-3 Assignment — Section A–D Standalone Solutions
Run each section independently to verify output.
"""

# ════════════════════════════════════════════════════════════════════════════════
# SECTION A — DECORATORS
# ════════════════════════════════════════════════════════════════════════════════

import time
import functools
import random


# ── Q1. @timer ────────────────────────────────────────────────────────────────
def timer(func):
    """Measures and prints execution time of the decorated function."""
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


# ── Q2. @retry ────────────────────────────────────────────────────────────────
def retry(max_attempts):
    """Retries the decorated function up to max_attempts times on exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    print(f"[retry] Attempt {attempt} succeeded!")
                    return result
                except Exception as e:
                    last_exc = e
                    print(f"[retry] Attempt {attempt} failed: {e}")
            raise Exception(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


random.seed(42)


@retry(max_attempts=5)
def fetch_data():
    """Simulates a flaky API call."""
    if random.choice([True, False]):
        raise ConnectionError("Server unreachable")
    return {"status": "ok", "data": [1, 2, 3]}


# ════════════════════════════════════════════════════════════════════════════════
# SECTION B — psycopg2
# ════════════════════════════════════════════════════════════════════════════════

def run_raw_query():
    """Connects to Supabase via psycopg2 and queries the users table."""
    import psycopg2
    from dotenv import load_dotenv
    import os

    load_dotenv()
    conn = None
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        print("Connected to Supabase successfully!")
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users LIMIT 5;")
            rows = cur.fetchall()
            print("Users (raw SQL):")
            for row in rows:
                print(row)
            print(f"Rows fetched: {len(rows)}")
    except psycopg2.errors.UndefinedTable:
        print("Error: 'users' table does not exist.")
    except Exception as e:
        print(f"Query failed: {e}")
    finally:
        if conn:
            conn.close()
            print("Connection closed.")


# ════════════════════════════════════════════════════════════════════════════════
# SECTION D — TRANSACTIONS & POOLING
# ════════════════════════════════════════════════════════════════════════════════

def create_user_with_tasks(session, username, email, password, task_titles):
    """
    Creates a user and their tasks in a single atomic transaction.
    Any failure triggers a full rollback — no partial data is saved.
    """
    from models.db_models import User, Task

    try:
        user = User(username=username, email=email, password=password)
        session.add(user)
        session.flush()  # Assigns user.id within the transaction (not yet committed)

        for title in task_titles:
            session.add(Task(title=title, owner_id=user.id))

        session.commit()
        return f"Transaction successful: User '{username}' created with {len(task_titles)} tasks"

    except Exception as e:
        session.rollback()
        return (
            f"Transaction rolled back: {e}\n"
            f"{email} was NOT saved"
        )


def demo_connection_pool():
    """Opens 3 sessions, prints pool status, then closes all."""
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    from dotenv import load_dotenv
    import os

    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")

    engine = create_engine(
        DATABASE_URL,
        pool_size=5,        # persistent connections kept alive
        max_overflow=10,    # extra connections allowed under load
        pool_timeout=30,    # wait time before raising on no available conn
        pool_recycle=1800,  # recycle after 30 min (Supabase idle timeout safety)
        pool_pre_ping=True, # health-check before handing out a connection
    )
    Session = sessionmaker(bind=engine)

    sessions = []
    for i in range(3):
        s = Session()
        s.execute(text("SELECT 1"))
        sessions.append(s)
        print(f"After opening session {i+1}: {engine.pool.status()}")

    for s in sessions:
        s.close()
    print(f"\nAfter closing all: {engine.pool.status()}")


# ════════════════════════════════════════════════════════════════════════════════
# QUICK DEMO (run this file directly)
# ════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("Q1 — @timer")
    print("=" * 60)
    result = compute_squares(1_000_000)
    print(f"Result: {result}")
    print(f"Function name: {compute_squares.__name__}")
    print(f"Docstring: {compute_squares.__doc__}")

    print("\n" + "=" * 60)
    print("Q2 — @retry")
    print("=" * 60)
    result = fetch_data()
    print(f"Result: {result}")
