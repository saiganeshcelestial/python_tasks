# LoanHub — Loan Application & Management System

A production-grade REST API built with **FastAPI**, **SQLAlchemy**, **PostgreSQL (Supabase)**, and **Alembic**.  
Authentication is handled via **JWT Bearer tokens** (python-jose + passlib/bcrypt).

---

## Project Structure

```
loanhub/
├── main.py                  # App entrypoint, lifespan, routers
├── config.py                # Pydantic BaseSettings (.env loader)
├── database.py              # Engine, SessionLocal, get_db()
├── models/
│   ├── enums.py             # UserRole, LoanPurpose, EmploymentStatus, LoanStatus
│   ├── db_models.py         # SQLAlchemy ORM models (User, Loan)
│   └── schemas.py           # Pydantic request/response schemas
├── services/
│   ├── user_service.py      # Registration, login, admin seeding
│   ├── loan_service.py      # Apply, review, list loans
│   └── analytics_service.py # Dashboard stats & aggregations
├── repositories/
│   ├── base_repository.py   # Abstract BaseRepository (ABC)
│   └── sqlalchemy_repository.py  # Concrete SQLAlchemy CRUD
├── routers/
│   ├── auth_router.py       # POST /auth/register, /auth/login
│   ├── loan_router.py       # /loans (user endpoints)
│   ├── admin_router.py      # /admin/loans (admin endpoints)
│   └── analytics_router.py  # /analytics/summary
├── decorators/
│   ├── timer.py             # @timer — logs execution time
│   ├── retry.py             # @retry(max_attempts) — DB connection
│   └── auth.py              # get_current_user(), require_role()
├── middleware/
│   └── logging_middleware.py  # Request logging to logs/app.log
├── exceptions/
│   └── custom_exceptions.py   # Custom exceptions + FastAPI handlers
├── utils/
│   ├── jwt_handler.py       # create_access_token(), decode_access_token()
│   └── notifications.py     # OCP strategy pattern, background tasks
├── alembic/                 # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 001_create_users_and_loans.py
│       └── 002_add_credit_score_to_loans.py
├── tests/
│   ├── conftest.py          # Fixtures, TestClient, SQLite override
│   ├── test_auth.py         # 8 auth tests
│   ├── test_loans.py        # 7 loan tests
│   └── test_admin.py        # 6 admin + analytics tests
├── logs/
│   ├── app.log
│   └── notifications.log
├── alembic.ini
├── requirements.txt
└── .env
```

---

## Quick Start

### 1. Clone and create virtual environment

```bash
git clone <repo-url>
cd loanhub
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env` and fill in your Supabase connection string and a strong secret key:

```bash
cp .env .env.local
```

Edit `.env`:
```
DATABASE_URL=postgresql://postgres:<password>@<host>:5432/postgres
SECRET_KEY=change-this-to-a-long-random-string
ADMIN_PASSWORD=your-admin-password
```

### 4. Run Alembic migrations

```bash
# Apply all migrations
alembic upgrade head

# To rollback the last migration
alembic downgrade -1

# Re-apply
alembic upgrade head
```

### 5. Start the server

```bash
uvicorn main:app --reload
```

The API is now available at `http://127.0.0.1:8000`.  
Interactive docs: `http://127.0.0.1:8000/docs`

---

## Authentication

All protected endpoints require a **Bearer token** in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Obtain the token from `POST /auth/login`.

| Role  | How to get token |
|-------|-----------------|
| User  | Register via `POST /auth/register`, then login |
| Admin | Login with `admin` / value of `ADMIN_PASSWORD` in `.env` |

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | Public | Register new user |
| POST | `/auth/login` | Public | Login — returns JWT |
| GET | `/health` | Public | DB health check |
| POST | `/loans` | User | Apply for a loan |
| GET | `/loans/my` | User | List my loans (filter + paginate) |
| GET | `/loans/my/{id}` | User | Single loan detail |
| GET | `/admin/loans` | Admin | All loans (filter + sort + paginate) |
| GET | `/admin/loans/{id}` | Admin | Any loan detail |
| PATCH | `/admin/loans/{id}/review` | Admin | Approve or reject |
| GET | `/analytics/summary` | Admin | Dashboard statistics |

---

## Running Tests

```bash
pytest tests/ -v
```

Tests use an in-memory **SQLite** database — no Supabase connection needed.

---

## Business Rules

- Loan amount: **₹1 – ₹10,00,000**
- Tenure: **6 – 360 months**
- Max **3 pending loans** per user at any time
- Only **pending** loans can be reviewed
- Admin must provide **remarks** (5–500 chars) when reviewing
- Admin account is **auto-seeded** on startup from `.env`
- JWT tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 30 min)

---

## Key Design Decisions

| Principle | Where Applied |
|-----------|--------------|
| **SRP** | Routers → HTTP only; Services → business logic; Repos → data access |
| **OCP** | `NotificationStrategy` — add channels without changing existing code |
| **LSP** | `SQLAlchemyRepository` is a drop-in for `BaseRepository` |
| **ISP** | `BaseRepository` defines only CRUD — no logging or notification methods |
| **DIP** | Services depend on `BaseRepository` abstraction, injected via `Depends()` |
| **JWT** | Stateless auth — `sub`, `user_id`, `role` in payload; validated on every request |
