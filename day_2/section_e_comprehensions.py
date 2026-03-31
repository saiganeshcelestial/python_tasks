# ============================================================
# Day-2 | Section E — Comprehensions & Utility Problems
# ============================================================

# ─────────────────────────────────────────────────────────────
# Q18. Filter and Transform with Dictionary Comprehension
# ─────────────────────────────────────────────────────────────
users = [
    {"username": "alice", "email": "a@b.com", "age": 25, "active": True},
    {"username": "bob",   "email": "b@b.com", "age": 17, "active": True},
    {"username": "carol", "email": "c@b.com", "age": 30, "active": False},
    {"username": "dave",  "email": "d@b.com", "age": 22, "active": True},
]

result = {u["username"]: u["email"] for u in users if u["active"] and u["age"] >= 18}
print("Q18:", result)  # {'alice': 'a@b.com', 'dave': 'd@b.com'}


# ─────────────────────────────────────────────────────────────
# Q19. Flatten and Deduplicate Tags
# ─────────────────────────────────────────────────────────────
articles = [
    {"title": "AI Intro",  "tags": ["python", "ml", "ai"]},
    {"title": "Web Dev",   "tags": ["python", "fastapi", "api"]},
    {"title": "Data 101",  "tags": ["ml", "pandas", "python"]},
]

unique_tags = sorted({tag for article in articles for tag in article["tags"]})
print("Q19:", unique_tags)  # ['ai', 'api', 'fastapi', 'ml', 'pandas', 'python']


# ─────────────────────────────────────────────────────────────
# Q20. Map HTTP Status Codes to Categories
# ─────────────────────────────────────────────────────────────
def classify(code):
    if 200 <= code < 300:   return "success"
    if 300 <= code < 400:   return "redirect"
    if 400 <= code < 500:   return "client_error"
    if 500 <= code < 600:   return "server_error"
    return "unknown"

codes = [200, 201, 404, 500, 301, 403, 502, 204]
result = [(code, classify(code)) for code in codes]
print("Q20:", result)
