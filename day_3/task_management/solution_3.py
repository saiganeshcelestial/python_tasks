# run_query.py
import psycopg2

from dotenv import load_dotenv
import os

load_dotenv()

def run_raw_query():
    conn = None
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        print("Connected to Supabase successfully!")
        
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM film LIMIT 5;")
            rows = cur.fetchall()
            
            print("title (raw SQL):")
            for row in rows:
                print(row)
            print(f"Rows fetched: {len(rows)}")

    except psycopg2.errors.UndefinedTable:
        print("Error: 'film' table does not exist.")
    except psycopg2.OperationalError as e:
        print(f"Connection failed: {e}")
    finally:
        if conn:
            conn.close()
            print("Connection closed.")

run_raw_query()