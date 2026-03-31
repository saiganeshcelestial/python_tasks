import json
import os
import threading
from typing import Optional
from repositories.base_repository import BaseRepository


class JSONRepository(BaseRepository):
    """
    Concrete JSON file-backed repository.
    LSP: fully substitutable for BaseRepository — no extra contracts broken.
    Thread-safe writes via a lock.
    """

    def __init__(self, filepath: str, collection_key: str):
        self._filepath = filepath
        self._collection_key = collection_key
        self._lock = threading.Lock()
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
        if not os.path.exists(self._filepath):
            self._write_raw({self._collection_key: []})

    def _load_raw(self) -> dict:
        try:
            with open(self._filepath, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Auto-recover from corrupted / missing file
            default = {self._collection_key: []}
            self._write_raw(default)
            return default

    def _write_raw(self, data: dict):
        with open(self._filepath, "w") as f:
            json.dump(data, f, indent=2)

    def _load(self) -> list:
        return self._load_raw().get(self._collection_key, [])

    def _save_all(self, records: list):
        with self._lock:
            raw = self._load_raw()
            raw[self._collection_key] = records
            self._write_raw(raw)

    # ── BaseRepository interface ──────────────────────────────

    def find_all(self) -> list:
        return self._load()

    def find_by_id(self, id: int) -> Optional[dict]:
        return next((r for r in self._load() if r["id"] == id), None)

    def save(self, record: dict) -> dict:
        records = self._load()
        records.append(record)
        self._save_all(records)
        return record

    def update(self, id: int, updates: dict) -> Optional[dict]:
        records = self._load()
        for i, r in enumerate(records):
            if r["id"] == id:
                records[i].update(updates)
                self._save_all(records)
                return records[i]
        return None

    def delete(self, id: int) -> bool:
        records = self._load()
        new_records = [r for r in records if r["id"] != id]
        if len(new_records) == len(records):
            return False
        self._save_all(new_records)
        return True

    def next_id(self) -> int:
        records = self._load()
        return max((r["id"] for r in records), default=0) + 1
