# ============================================================
# Python Day-1 Assignment Solutions
# ============================================================

# ─────────────────────────────────────────────────────────────
# 1. Remove Duplicates While Preserving Order (no set())
# ─────────────────────────────────────────────────────────────
def remove_duplicates(nums):
    seen = {}
    result = []
    for n in nums:
        if n not in seen:
            seen[n] = True
            result.append(n)
    return result

# Test
nums = [1, 2, 2, 3, 4, 4, 5]
print("1.", remove_duplicates(nums))  # [1, 2, 3, 4, 5]


# ─────────────────────────────────────────────────────────────
# 2. Second Largest Unique Element (no sorting, O(n))
# ─────────────────────────────────────────────────────────────
def second_largest(nums):
    first = second = float('-inf')
    for n in nums:
        if n > first:
            second = first
            first = n
        elif first > n > second:
            second = n
    return second if second != float('-inf') else None

# Test
nums = [10, 20, 4, 45, 99, 99]
print("2.", second_largest(nums))  # 45


# ─────────────────────────────────────────────────────────────
# 3. Group Anagrams
# ─────────────────────────────────────────────────────────────
def group_anagrams(words):
    groups = {}
    for word in words:
        key = ''.join(sorted(word))
        groups.setdefault(key, []).append(word)
    return list(groups.values())

# Test
words = ["eat", "tea", "tan", "ate", "nat", "bat"]
print("3.", group_anagrams(words))  # [['eat','tea','ate'],['tan','nat'],['bat']]


# ─────────────────────────────────────────────────────────────
# 4. Top K Frequent Elements (bucket sort — O(n))
# ─────────────────────────────────────────────────────────────
def top_k_frequent(nums, k):
    freq = {}
    for n in nums:
        freq[n] = freq.get(n, 0) + 1

    buckets = [[] for _ in range(len(nums) + 1)]
    for num, count in freq.items():
        buckets[count].append(num)

    result = []
    for i in range(len(buckets) - 1, 0, -1):
        result.extend(buckets[i])
        if len(result) >= k:
            break
    return result[:k]

# Test
nums = [1, 1, 1, 2, 2, 3]
k = 2
print("4.", top_k_frequent(nums, k))  # [1, 2]


# ─────────────────────────────────────────────────────────────
# 5. Word Frequency Counter (File Handling)
# ─────────────────────────────────────────────────────────────
import string

def word_frequency(filepath):
    freq = {}
    with open(filepath, 'r') as f:
        for line in f:
            words = line.lower().split()
            for word in words:
                word = word.strip(string.punctuation)
                if word:
                    freq[word] = freq.get(word, 0) + 1
    return freq

# Usage (requires a .txt file):
# print("5.", word_frequency("sample.txt"))


# ─────────────────────────────────────────────────────────────
# 6. JSON Validation
# ─────────────────────────────────────────────────────────────
import json

def is_valid_json(s):
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False

# Test
print("6a.", is_valid_json('{"name": "John", "age": 30}'))   # True
print("6b.", is_valid_json('{"name": "John", "age": }'))     # False


# ─────────────────────────────────────────────────────────────
# 7. Custom Exception Handling
# ─────────────────────────────────────────────────────────────
class SalaryTooLowError(Exception):
    pass

def validate_salary(salary):
    if salary < 10000:
        raise SalaryTooLowError("SalaryTooLowError")

# Test
try:
    validate_salary(8000)
except SalaryTooLowError as e:
    print("7.", e)  # SalaryTooLowError


# ─────────────────────────────────────────────────────────────
# 8. Flatten Nested List (Recursive)
# ─────────────────────────────────────────────────────────────
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# Test
nested = [1, [2, [3, 4], 5], 6]
print("8.", flatten(nested))  # [1, 2, 3, 4, 5, 6]


# ─────────────────────────────────────────────────────────────
# 9. Lambda + Sorting Complex Structure
# ─────────────────────────────────────────────────────────────
people = [{'name': 'A', 'age': 30}, {'name': 'B', 'age': 20}]
sorted_people = sorted(people, key=lambda x: x['age'])
print("9.", sorted_people)  # [{'name':'B','age':20},{'name':'A','age':30}]


# ─────────────────────────────────────────────────────────────
# 10. Environment Variables Loader
# ─────────────────────────────────────────────────────────────
def load_env(filepath):
    env = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env[key.strip()] = value.strip()
    return env

# Usage (requires a .env file):
# print("10.", load_env(".env"))


# ─────────────────────────────────────────────────────────────
# 11. Logging System
# ─────────────────────────────────────────────────────────────
from datetime import datetime

def log_error(message, filepath="errors.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} ERROR {message}\n"
    with open(filepath, 'a') as f:
        f.write(entry)
    print("11. Logged:", entry.strip())

# Test
log_error("Something failed")


# ─────────────────────────────────────────────────────────────
# 12. Create Dictionary from Two Lists (comprehension)
# ─────────────────────────────────────────────────────────────
keys = ['a', 'b', 'c']
values = [1, 2, 3]
result = {k: v for k, v in zip(keys, values)}
print("12.", result)  # {'a':1,'b':2,'c':3}


# ─────────────────────────────────────────────────────────────
# 13. Invert Dictionary Using Comprehension
# ─────────────────────────────────────────────────────────────
d = {'a': 1, 'b': 2, 'c': 3}
inverted = {v: k for k, v in d.items()}
print("13.", inverted)  # {1:'a',2:'b',3:'c'}


# ─────────────────────────────────────────────────────────────
# 14. Extract Words Starting with Vowel
# ─────────────────────────────────────────────────────────────
sentence = "apple banana orange grape"
vowels = set('aeiouAEIOU')
result = [w for w in sentence.split() if w[0] in vowels]
print("14.", result)  # ['apple', 'orange']


# ─────────────────────────────────────────────────────────────
# 15. Replace Negative Numbers with 0
# ─────────────────────────────────────────────────────────────
nums = [1, -2, 3, -4, 5]
result = [n if n >= 0 else 0 for n in nums]
print("15.", result)  # [1, 0, 3, 0, 5]


# ─────────────────────────────────────────────────────────────
# 16. Multi-condition List Comprehension
# ─────────────────────────────────────────────────────────────
result = [n for n in range(1, 20) if n % 2 == 0 and n % 3 == 0]
print("16.", result)  # [6, 12, 18]


# ============================================================
# OOP Problems
# ============================================================

# ─────────────────────────────────────────────────────────────
# 17. Smart Banking System (OOP + SRP + Encapsulation)
# ─────────────────────────────────────────────────────────────
class TransactionLogger:
    def log(self, action, amount, balance):
        print(f"[LOG] {action}: ₹{amount} | Balance: ₹{balance}")


class Account:
    def __init__(self, owner, initial_balance=0):
        self.__owner = owner
        self.__balance = initial_balance
        self._logger = TransactionLogger()

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance += amount
        self._logger.log("Deposit", amount, self.__balance)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient funds.")
        self.__balance -= amount
        self._logger.log("Withdrawal", amount, self.__balance)

    def get_balance(self):
        print(f"Balance: {self.__balance}")
        return self.__balance


class SavingsAccount(Account):
    pass


# Test
acc = SavingsAccount("John", 1000)
acc.deposit(500)
acc.withdraw(200)
acc.get_balance()  # Balance: 1300


# ─────────────────────────────────────────────────────────────
# 18. Bird System Fix (LSP + Inheritance Design)
# ─────────────────────────────────────────────────────────────
class Bird:
    def move(self):
        raise NotImplementedError

class FlyingBird(Bird):
    def move(self):
        return f"{self.__class__.__name__} flies"

class SwimmingBird(Bird):
    def move(self):
        return f"{self.__class__.__name__} swims"

class Sparrow(FlyingBird):
    pass

class Penguin(SwimmingBird):
    pass

# Test
birds = [Sparrow(), Penguin()]
for bird in birds:
    print("18.", bird.move())


# ─────────────────────────────────────────────────────────────
# 19. E-Commerce Checkout System (ALL SOLID Principles)
# ─────────────────────────────────────────────────────────────

# Abstraction (DIP / ISP)
class PaymentMethod:
    def pay(self, amount):
        raise NotImplementedError

class DiscountStrategy:
    def apply(self, amount):
        raise NotImplementedError

class Logger:
    def log(self, message):
        raise NotImplementedError

# Payment implementations (OCP)
class UPI(PaymentMethod):
    def pay(self, amount):
        print(f"Payment Successful via UPI")

class Card(PaymentMethod):
    def pay(self, amount):
        print(f"Payment Successful via Card")

# Discount implementations (OCP)
class FestivalDiscount(DiscountStrategy):
    def apply(self, amount):
        return amount * 0.9  # 10% off

class PremiumDiscount(DiscountStrategy):
    def apply(self, amount):
        return amount * 0.85  # 15% off

class NoDiscount(DiscountStrategy):
    def apply(self, amount):
        return amount

# Logger (SRP)
class ConsoleLogger(Logger):
    def log(self, message):
        print(message)

# Checkout (SRP + DIP)
class Checkout:
    def __init__(self, payment: PaymentMethod, discount: DiscountStrategy, logger: Logger = None):
        self._payment = payment
        self._discount = discount
        self._logger = logger or ConsoleLogger()

    def process(self, amount):
        final = self._discount.apply(amount)
        self._logger.log(f"Final Amount: {int(final)}")
        self._payment.pay(final)

# Test
checkout = Checkout(payment=UPI(), discount=FestivalDiscount())
checkout.process(1000)
# Final Amount: 900
# Payment Successful via UPI
