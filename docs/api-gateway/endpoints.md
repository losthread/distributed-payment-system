# API Gateway API

**Base URL:** `/`

## Endpoints

### GET /

API gateway health check.

**Auth:** None

**Response:**

```json
{
  "message": "API Gateway is running!"
}
```

### Auth Service — `/auth`, `/users`

Proxy to Auth Service.

| Method   | Path                  | Auth   | Description                    |
|----------|-----------------------|--------|--------------------------------|
| POST     | `/auth/register`      | -      | Register, returns JWT          |
| POST     | `/auth/login`         | -      | Email/password login           |
| POST     | `/auth/login/google`  | -      | Google OAuth login             |
| GET      | `/users/profile`      | JWT    | Get profile                    |
| PATCH    | `/users/profile`      | JWT    | Update profile                 |
| DELETE   | `/users/profile`      | JWT    | Delete account                 |

### Wallet Service — `/wallets`, `/internal`

Proxy to Wallet Service.

| Method   | Path                                 | Auth            | Description                            |
|----------|--------------------------------------|-----------------|----------------------------------------|
| GET      | `/wallets`                           | JWT             | Get wallet                             |
| GET      | `/wallets/balance`                   | JWT             | Get balance                            |
| POST     | `/wallets/deposit`                   | JWT             | Deposit to own wallet                  |
| POST     | `/wallets/withdraw`                  | JWT             | Withdraw from own wallet               |

### Transaction Service — `/transactions`

Proxy to Transaction Service.

| Method | Path                          | Auth | Description                          |
|--------|-------------------------------|------|--------------------------------------|
| POST   | `/transactions`               | JWT  | Send money (debit + credit)          |
| GET    | `/transactions`               | JWT  | List user's transactions             |
| GET    | `/transactions/{id}`          | JWT  | Get transaction detail               |

Transaction statuses: `pending` → `completed` | `failed` | `refund_failed`

### Notification Service — `/notifications`

Proxy to Notification Service.

| Method   | Path                          | Auth   | Description                                |
|----------|-------------------------------|--------|--------------------------------------------|
| GET      | `/notifications`              | JWT    | Get all notifications for user             |
| PATCH    | `/notifications/read-all`     | JWT    | Mark all notifications as read             |
| DELETE   | `/notifications/delete-all`   | JWT    | Delete all notifications                   |
| GET      | `/notifications/{id}`         | JWT    | Get specific notification                  |
| PATCH    | `/notifications/{id}/read`    | JWT    | Mark specific notification as read         |
| DELETE   | `/notifications/{id}`         | JWT    | Delete specific notification               |