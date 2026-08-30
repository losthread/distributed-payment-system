# Wallet Service API

**Base URL:** `/wallets`

## Endpoints

### GET `/wallets`

Get authenticated user wallet.

**Auth:** JWT token required

**Response:**

```json
{
  "id": 1,
  "user_id": "uuid",
  "balance": "decimal",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### GET `/wallets/balance`

Get authenticated user wallet balance.

**Auth:** JWT token required

**Response:**

```json
{
  "balance": "decimal"
}
```

### POST `/wallets/deposit`

Deposit money into authenticated user wallet.

**Auth:** JWT token required

**Request:**

```json
{
  "amount": "decimal"
}
```

**Response:**

```json
{
  "balance": "decimal"
}
```

### POST `/wallets/withdraw`

Withdraw money from authenticated user wallet.

**Auth:** JWT token required

**Request:**

```json
{
  "amount": "decimal"
}
```

**Response:**

```json
{
  "balance": "decimal"
}
```

## Internal Endpoints

**Base URL:** `/internal`

### GET `/internal/wallets/{user_id}`

Get specific user wallet.

**Auth:** Internal service token required

**Response:**

```json
{
  "user_id": "uuid",
  "balance": "decimal"
}
```

### POST `/internal/wallets/{user_id}/debit`

Debit money from specific user wallet.

**Auth:** Internal service token required

**Request:**

```json
{
  "amount": "decimal"
}
```

**Response:**

```json
{
  "user_id": "uuid",
  "balance": "decimal"
}
```

### POST `/internal/wallets/{user_id}/credit`

Credit money to specific user wallet.

**Auth:** Internal service token required

**Request:**

```json
{
  "amount": "decimal"
}
```

**Response:**

```json
{
  "user_id": "uuid",
  "balance": "decimal"
}
```
