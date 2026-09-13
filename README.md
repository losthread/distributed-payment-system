# Distributed Payment System

A microservices-based payment system with auth, wallets, and transactions, built in Python/FastAPI.

## Architecture

```text
                                   ┌──────────────┐
                                   │    Clients   │
                                   └───────┬──────┘
                                           │
                                           ▼
                                 ┌───────────────────┐
                                 │     API Gateway   │
                                 │  +(Rate Limiting) │
                                 └────────┬──────────┘
                                          │
              ┌────────────────┬──────────┼─────┬───────────────────┐
              ▼                ▼                ▼                   ▼
       ┌────────────┐   ┌────────────┐   ┌──────────────┐   ┌───────────────┐
       │    Auth    │   │   Wallet   │   │ Transaction  │   │  Notification │
       │  Service   │   │  Service   │   │   Service    │   │   Service     │
       └─┬─────┬────┘   └──────┬─────┘   └──────────────┘   └───────────────┘
         │     │             ▲ │  ▲               ▲  │              ▲
         │     ▼   ┌───────┐ │ │  ▼               ▼  │              │
         │     └───│ Kafka │─┘ │  │               │  │              │
         │         └───────┘   │  │               │  │              │
         │                     │  │    ┌───────┐  │  │              │
         │                     │  └────│ Kafka │  │  │              │
         │                     │       │ + APIs│──┘  │              │
         │                     │       └───────┘     │              │
         │                     │                     │              │
         ▼                     ▼     ┌──────────┐    ▼              │  
         └───────────────────────────│          │────┘              │         
                                     │  Kafka   │                   │  
                                     │          │───────────────────┘
                                     └──────────┘
```

Three services share a JWT secret and an internal service token; the Wallet Service is the only service that runs a long-lived Kafka consumer.

| Service                 | Port | DB              | Responsibility                              |
|-------------------------|------|-----------------|---------------------------------------------|
| Auth Service            | 8000 | auth_db         | Registration, login, JWT issuance, OAuth    |
| Wallet Service          | 8001 | wallet_db       | Wallet CRUD, deposits, withdrawals, refunds |
| Transaction Service     | 8002 | transactions_db | Money transfers, transaction lifecycle      |
| Notification Service    | 8004 | notification_db | User Notifications                          |
| API Gateway             | 8006 |        -        | Frontend entrypoint, rate limiting          |

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

### Notification Service — `/notifications`

| Method   | Path                          | Auth   | Description                                |
|----------|-------------------------------|--------|--------------------------------------------|
| GET      | `/notifications`              | JWT    | Get all notifications for user             |
| PATCH    | `/notifications/read-all`     | JWT    | Mark all notifications as read             |
| DELETE   | `/notifications/delete-all`   | JWT    | Delete all notifications                   |
| GET      | `/notifications/{id}`         | JWT    | Get specific notification                  |
| PATCH    | `/notifications/{id}/read`    | JWT    | Mark specific notification as read         |
| DELETE   | `/notifications/{id}`         | JWT    | Delete specific notification               |

## Running the Project

## Clone the Repository

```bash
git clone https://github.com/losthread/distributed-payment-system.git
cd distributed-payment-system

## Running With Docker

```bash
# Orchestrate services
# build and start
docker compose up -d --build
# start without rebuilding
docker compose up -d
# view running services
docker compose ps
# stop containers
docker compose down
```

## Running Without Docker

```bash
# create a virtual environment
python3 -m venv .venv
source .venv/bin/activate
# instal dependencies
pip install -r requirements.txt
# create a .env file inside each service directory like .env.example and configure environment variables
touch .env
# make sure PostgreSQL, Kafka and Redis are running before starting the services
# run each service in a separate terminal
uvicorn app.core.main:app --reload --host 0.0.0.0 --port <PORT>
# once all services are running use the API gateway to interact with the application
```

## Project Structure

```text
.
├ docker-compose.yaml
├ docs/
│   ├── api-service/
│   ├── auth-service/
│   ├── notification-service/
│   ├── transaction-service/
│   └── wallet-service/
├ api-gateway/
├ auth-service/
├ wallet-service/
├ notification-service/
└ transactions-service/
```

Each service follows the same layout: `app/{core,crud,models,routes,tests}/`.

## Tech Stack

- **Framework:** FastAPI
- **DB:** PostgreSQL (psycopg3)
- **Auth:** JWT (PyJWT), Argon2 password hashing, Google OAuth
- **Messaging:** Kafka (confluent-kafka)
- **Rate Limiting:** Redis (Token Bucket Algorithm)
- **Validation:** Pydantic
