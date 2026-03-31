# ============================================================
# Day-2 | Section B — SOLID Principles
# ============================================================
import json
import os
from abc import ABC, abstractmethod


# ─────────────────────────────────────────────────────────────
# Q4. SRP — UserValidator, UserStorage, UserNotifier
# ─────────────────────────────────────────────────────────────
class UserValidator:
    def validate(self, data: dict):
        if not data.get("username"):
            raise ValueError("Username is required.")
        if "@" not in data.get("email", "") or "." not in data.get("email", ""):
            raise ValueError("Invalid email format.")
        print("Validation passed")


class UserStorage:
    def __init__(self, filepath="users.json"):
        self.filepath = filepath

    def save(self, data: dict):
        users = []
        if os.path.exists(self.filepath):
            with open(self.filepath) as f:
                users = json.load(f).get("users", [])
        users.append(data)
        with open(self.filepath, "w") as f:
            json.dump({"users": users}, f, indent=2)
        print(f"User saved to {self.filepath}")


class UserNotifier:
    def notify(self, email: str):
        print(f"Welcome email sent to {email}")


def register_user(data: dict):
    validator = UserValidator()
    storage = UserStorage()
    notifier = UserNotifier()

    validator.validate(data)
    storage.save(data)
    notifier.notify(data["email"])


# Test Q4
print("--- Q4 ---")
register_user({"username": "alice", "email": "alice@mail.com"})
print()


# ─────────────────────────────────────────────────────────────
# Q5. OCP — Extensible Discount System
# ─────────────────────────────────────────────────────────────
class Discount(ABC):
    @abstractmethod
    def apply(self, amount: float) -> float:
        pass


class NoDiscount(Discount):
    def apply(self, amount: float) -> float:
        return amount


class PercentageDiscount(Discount):
    def apply(self, amount: float) -> float:
        return max(0, amount * 0.90)


class FlatDiscount(Discount):
    def apply(self, amount: float) -> float:
        return max(0, amount - 200)


class BuyOneGetOneFree(Discount):
    def apply(self, amount: float) -> float:
        return max(0, amount * 0.50)


def calculate_total(amount: float, discount: Discount) -> float:
    return discount.apply(amount)


# Test Q5
print("--- Q5 ---")
print(calculate_total(1000, PercentageDiscount()))  # 900.0
print(calculate_total(1000, FlatDiscount()))        # 800.0
print(calculate_total(1000, BuyOneGetOneFree()))    # 500.0
print()


# ─────────────────────────────────────────────────────────────
# Q6. LSP — Fix the Bird Hierarchy
# ─────────────────────────────────────────────────────────────
class Bird(ABC):
    @abstractmethod
    def move(self):
        pass


class FlyingBird(Bird):
    def move(self):
        return f"{self.__class__.__name__} flies"


class SwimmingBird(Bird):
    def move(self):
        return f"{self.__class__.__name__} swims"


class FlyingSwimmingBird(Bird):
    def move(self):
        return f"{self.__class__.__name__} flies and swims"


class Sparrow(FlyingBird):
    pass


class Eagle(FlyingBird):
    pass


class Penguin(SwimmingBird):
    pass


class Duck(FlyingSwimmingBird):
    pass


# Test Q6
print("--- Q6 ---")
for bird in [Sparrow(), Eagle(), Penguin(), Duck()]:
    print(bird.move())
print()


# ─────────────────────────────────────────────────────────────
# Q7. DIP — Repository Pattern with Dependency Injection
# ─────────────────────────────────────────────────────────────
class UserRepository(ABC):
    @abstractmethod
    def save(self, user: dict):
        pass

    @abstractmethod
    def find(self, username: str):
        pass


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._store = {}

    def save(self, user: dict):
        self._store[user["username"]] = user

    def find(self, username: str):
        return self._store.get(username)


class JSONUserRepository(UserRepository):
    def __init__(self, filepath="repo_users.json"):
        self.filepath = filepath

    def _load(self):
        if not os.path.exists(self.filepath):
            return {}
        with open(self.filepath) as f:
            return json.load(f)

    def _write(self, data):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    def save(self, user: dict):
        data = self._load()
        data[user["username"]] = user
        self._write(data)

    def find(self, username: str):
        return self._load().get(username)


class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    def register(self, user: dict):
        self._repo.save(user)

    def get_user(self, username: str):
        return self._repo.find(username)


# Test Q7
print("--- Q7 ---")
repo = InMemoryUserRepository()
service = UserService(repo)
service.register({"username": "alice", "email": "a@b.com"})
print(service.get_user("alice"))  # {'username': 'alice', 'email': 'a@b.com'}
