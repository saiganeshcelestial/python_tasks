import asyncio
import logging
import json
from datetime import datetime, timezone
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
notification_logger = logging.getLogger("notifications")

# In-memory counter for reviews processed today
reviews_today_counter: dict = {"count": 0}


# ─── OCP: Notification Strategy (Open/Closed Principle) ──────────────────────

class NotificationStrategy(ABC):
    @abstractmethod
    async def send(self, event_type: str, payload: dict) -> None:
        pass


class ConsoleNotification(NotificationStrategy):
    async def send(self, event_type: str, payload: dict) -> None:
        print(f"[NOTIFICATION] {event_type}: {payload}")


class LogFileNotification(NotificationStrategy):
    async def send(self, event_type: str, payload: dict) -> None:
        notification_logger.info(
            f"[{datetime.now(timezone.utc).isoformat()}] "
            f"{event_type} | loan_id={payload.get('loan_id')} "
            f"user='{payload.get('username')}' | {payload.get('detail', '')}"
        )


class EventLogNotification(NotificationStrategy):
    """Writes structured JSON events to logs/events.jsonl"""
    async def send(self, event_type: str, payload: dict) -> None:
        event = {
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **payload,
        }
        try:
            with open("logs/events.jsonl", "a") as f:
                f.write(json.dumps(event) + "\n")
        except Exception as exc:
            logger.error(f"EventLogNotification failed: {exc}")


# Active strategies — add new ones here without touching existing code
_strategies: list[NotificationStrategy] = [
    ConsoleNotification(),
    LogFileNotification(),
    EventLogNotification(),
]


# ─── Async multi-channel simulation ──────────────────────────────────────────

async def _simulate_email(payload: dict):
    await asyncio.sleep(0.05)
    logger.info(f"[EMAIL] Sent notification to user {payload.get('username')}")


async def _simulate_sms(payload: dict):
    await asyncio.sleep(0.03)
    logger.info(f"[SMS] Sent SMS to user {payload.get('username')}")


async def _simulate_push(payload: dict):
    await asyncio.sleep(0.02)
    logger.info(f"[PUSH] Sent push notification to user {payload.get('username')}")


async def _dispatch_all_strategies(event_type: str, payload: dict):
    await asyncio.gather(*[s.send(event_type, payload) for s in _strategies])


async def _run_all_channels(payload: dict):
    await asyncio.gather(
        _simulate_email(payload),
        _simulate_sms(payload),
        _simulate_push(payload),
    )


# ─── Public background task functions ────────────────────────────────────────

def notify_loan_reviewed(loan_id: int, username: str, status: str):
    """Background task: fired when admin approves/rejects a loan."""
    reviews_today_counter["count"] += 1
    payload = {
        "loan_id": loan_id,
        "username": username,
        "detail": f"Loan #{loan_id} for user '{username}' has been {status} — notification sent",
    }
    asyncio.run(_dispatch_all_strategies(f"loan_{status}", payload))
    asyncio.run(_run_all_channels(payload))
    logger.info(f"Reviews processed today: {reviews_today_counter['count']}")


def notify_loan_applied(loan_id: int, username: str, purpose: str, amount: int):
    """Background task: fired when a user submits a new loan application."""
    payload = {
        "loan_id": loan_id,
        "username": username,
        "detail": f"New loan application #{loan_id} by '{username}' for {purpose} — ₹{amount}",
    }
    asyncio.run(_dispatch_all_strategies("loan_applied", payload))
