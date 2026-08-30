# Transaction Service API

**Base URL:** `/transactions`

## Endpoints

### POST `/transactions`

Send money to a customer.

**Auth:** JWT token required

**Request:**

```json
{
  "receiver_id": "uuid",
  "amount": "decimal"
}
```

**Response:**

```json
{
  "transaction_id": "uuid",
  "sender_id": "uuid",
  "receiver_id": "uuid",
  "amount": "decimal",
  "status": "pending|completed|failed|refund_failed",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### GET `/transactions`

Get all transactions for authenticated user.

**Auth:** JWT token required

**Response:**

```json
[
  {
    "transaction_id": "uuid",
    "sender_id": "uuid",
    "receiver_id": "uuid",
    "amount": "decimal",
    "status": "pending|completed|failed|refund_failed",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### GET `/transactions/{transaction_id}`

Get specific transaction details.

**Auth:** JWT token required

**Response:**

```json
{
  "transaction_id": "uuid",
  "sender_id": "uuid",
  "receiver_id": "uuid",
  "amount": "decimal",
  "status": "pending|completed|failed|refund_failed",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```
