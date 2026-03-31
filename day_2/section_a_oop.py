# ============================================================
# Day-2 | Section A — OOP & Encapsulation
# ============================================================

# ─────────────────────────────────────────────────────────────
# Q1. User Profile with Encapsulation
# ─────────────────────────────────────────────────────────────
class User:
    def __init__(self, username, email, age):
        self._username = username
        self.set_email(email)
        self.set_age(age)

    # --- Email ---
    def get_email(self):
        return self._email

    def set_email(self, email):
        if '@' not in email or '.' not in email:
            raise ValueError("Invalid email format")
        self._email = email

    # --- Age ---
    def get_age(self):
        return self._age

    def set_age(self, age):
        if not (18 <= age <= 120):
            raise ValueError("Age must be between 18 and 120")
        self._age = age

    # --- Username ---
    def get_username(self):
        return self._username


# Test Q1
try:
    user = User("alice", "alice@mail.com", 25)
    user.set_email("invalid")
except ValueError as e:
    print(f"ValueError: {e}")

try:
    user.set_age(150)
except ValueError as e:
    print(f"ValueError: {e}")

print(user.get_email())   # alice@mail.com
print(user.get_age())     # 25
print()


# ─────────────────────────────────────────────────────────────
# Q2. Inheritance — AdminUser and CustomerUser
# ─────────────────────────────────────────────────────────────
class BaseUser:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def display_profile(self):
        print(f"User: {self.username} | Role: {self.role}")


class AdminUser(BaseUser):
    def __init__(self, username, permissions):
        super().__init__(username, "admin")
        self.permissions = permissions

    def display_profile(self):
        perms = ", ".join(self.permissions)
        print(f"Admin: {self.username} | Permissions: {perms}")


class CustomerUser(BaseUser):
    def __init__(self, username, orders):
        super().__init__(username, "customer")
        self.orders = orders

    def display_profile(self):
        print(f"Customer: {self.username} | Orders: {self.orders}")


# Test Q2
admin = AdminUser("admin1", ["manage_users", "view_logs"])
customer = CustomerUser("cust1", 5)
admin.display_profile()     # Admin: admin1 | Permissions: manage_users, view_logs
customer.display_profile()  # Customer: cust1 | Orders: 5
print()


# ─────────────────────────────────────────────────────────────
# Q3. Composition — Order with Address, PaymentInfo, OrderItem
# ─────────────────────────────────────────────────────────────
class Address:
    def __init__(self, city, zip_code):
        self.city = city
        self.zip_code = zip_code


class PaymentInfo:
    def __init__(self, method, amount):
        self.method = method
        self.amount = amount


class OrderItem:
    def __init__(self, name, qty, price):
        self.name = name
        self.qty = qty
        self.price = price

    def total(self):
        return self.qty * self.price


class Order:
    def __init__(self, address: Address, payment: PaymentInfo, items: list):
        self.address = address
        self.payment = payment
        self.items = items

    def order_summary(self):
        print(f"Shipping: {self.address.city} - {self.address.zip_code}")
        item_str = ", ".join(
            f"{item.name} x{item.qty} = {item.total()}" for item in self.items
        )
        print(f"Items: {item_str}")
        total = sum(item.total() for item in self.items)
        print(f"Total: {total}")
        print(f"Payment: {self.payment.method}")


# Test Q3
addr = Address("Bangalore", "560001")
pay = PaymentInfo("UPI", 1500)
items = [OrderItem("Book", 2, 500), OrderItem("Pen", 5, 100)]
order = Order(addr, pay, items)
order.order_summary()
