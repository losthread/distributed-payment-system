# Distributed Payment System

A microservices-based payment system with auth, wallets, and transactions, built in Python/FastAPI.

## Architecture

```text
┌────────────┐     ┌─────────────┐
│  Clients   │────▶│  Auth Svc   │─── JWT ───▶
└────────────┘     └─────┬───────┘
                         │
         ┌───────────────┼─────────────────┐
         ▼               ▼                 ▼
   ┌──────────┐    ┌──────────┐      ┌──────────┐
   │ Wallet   │    │ Wallet   │      │   Kafka  │
   │ Service  │    │ Service  │      │          │
   └──────────┘    └──────────┘      └────┬─────┘
         │               │                │
         └───────────────┼────────────────┘
                         ▼
                   ┌───────────┐
                   │Transaction│
                   │ Service   │
                   └───────────┘
```

Three services share a JWT secret and an internal service token; the Wallet Service is the only service that runs a long-lived Kafka consumer.

| Service             | Port | DB                      | Responsibility                              |
|---------------------|------|-------------------------|---------------------------------------------|
| Auth Service        | 8000 | auth_service_db         | Registration, login, JWT issuance, OAuth    |
| Wallet Service      | 8001 | wallet_service_db       | Wallet CRUD, deposits, withdrawals, refunds |
| Transaction Service | 8002 | transactions_service_db | Money transfers, transaction lifecycle      |

## Event Flow (Kafka)

```text
Auth Service          user.created ─────────────────────▶ Kafka ──▶ Wallet Service
                                              (creates wallet, balance 0.00)

Transaction Service ─ debit ─► Wallet Service
Transaction Service ─ credit ─► Wallet Service
   │ credit fails │ refund fails ──► refund.requested ──► Kafka ──▶ Wallet Service
                                                        (retries 3x, emits refund.completed / refund.failed)
```

## API

### Auth Service — `/auth`, `/users`

| Method   | Path                  | Auth   | Description                    |
|----------|-----------------------|--------|--------------------------------|
| POST     | `/auth/register`      | -      | Register, returns JWT          |
| POST     | `/auth/login`         | -      | Email/password login           |
| POST     | `/auth/login/google`  | -      | Google OAuth login             |
| GET      | `/users/profile`      | JWT    | Get profile                    |
| PATCH    | `/users/profile`      | JWT    | Update profile                 |
| DELETE   | `/users/profile`      | JWT    | Delete account                 |

### Wallet Service — `/wallets`, `/internal`

| Method   | Path                                 | Auth            | Description                            |
|----------|--------------------------------------|-----------------|----------------------------------------|
| GET      | `/wallets`                           | JWT             | Get wallet                             |
| GET      | `/wallets/balance`                   | JWT             | Get balance                            |
| POST     | `/wallets/deposit`                   | JWT             | Deposit to own wallet                  |
| POST     | `/wallets/withdraw`                  | JWT             | Withdraw from own wallet               |
| GET      | `/internal/wallets/{user_id}`        | Internal token  | Get any user's wallet                  |
| POST     | `/internal/wallets/{user_id}/debit`  | Internal token  | Debit any wallet (by Transaction Svc)  |
| POST     | `/internal/wallets/{user_id}/credit` | Internal token  | Credit any wallet (by Transaction Svc) |

### Transaction Service — `/transactions`

| Method | Path                          | Auth | Description                          |
|--------|-------------------------------|------|--------------------------------------|
| POST   | `/transactions`               | JWT  | Send money (debit + credit)          |
| GET    | `/transactions`               | JWT  | List user's transactions             |
| GET    | `/transactions/{id}`          | JWT  | Get transaction detail               |

Transaction statuses: `pending` → `completed` | `failed` | `refund_failed`

## Running

```bash
# Start Kafka
docker compose up -d

# In each service directory
cd auth-service && pip install -r requirements.txt && uvicorn app.main:app --reload -p 8000
cd wallet-service  && pip install -r requirements.txt && uvicorn app.main:app --reload -p 8001
cd transactions-service && pip install -r requirements.txt && uvicorn app.main:app --reload -p 8002
```

Apply DB schema in each service before running:

```bash
psql $DATABASE_URL < schema.sql
```

## Project Structure

```text
.
├── docker-compose.yaml   # Kafka (single broker)
├── docs/
│   ├── auth-service/
│   ├── transaction-service/
│   └── wallet-service/
├── auth-service/
├── wallet-service/
└── transactions-service/
```

> Note: Microservices are not containerized yet

Each service follows the same layout: `app/{core,crud,models,routes,tests}/`.

## Tech Stack

- **Framework:** FastAPI
- **DB:** PostgreSQL (psycopg3)
- **Auth:** JWT (PyJWT), Argon2 password hashing, Google OAuth
- **Messaging:** Kafka (confluent-kafka)
- **Validation:** Pydantic
