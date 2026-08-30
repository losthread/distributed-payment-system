# Auth Service API

**Base URL:** `/auth`

## Endpoints

### POST `/auth/register`

Register new user.
**Request:**

```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```

**Response:**

```json
{ 
  "user_id": "uuid",
  "token": "jwt"
}
```

### POST `/auth/login`

Login with email & password.

**Request:**

```json
{
  "email": "user@example.com",
  "password": "string"
}
```

**Response:**

```json
  { 
    "user_id": "uuid", 
    "token": "jwt" 
  }
```

### POST `/auth/login/google`

Login with Google token.

**Request:**

```json
{
  "token": "google_id_token"
}
```

**Response:**

```json
  {
    "user_id": "uuid",
    "token": "jwt" 
  }
```

## User Endpoints

**Base URL:** `/users`

### GET `/users/profile`

Get authenticated user profile.

**Auth:** JWT token required

**Response:**

```json
{
  "user_id": "uuid",
  "username": "string",
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### PATCH `/users/profile`

Update authenticated user profile.

**Auth:** JWT token required

**Request:**

```json
{
  "username": "string",
  "email": "user@example.com"
}
```

**Response:** Updated user profile (same as GET)

### DELETE `/users/profile`

Delete authenticated user profile.

**Auth:** JWT token required

**Response:**

```json
  {
    "message": "Profile deleted" 
  }
```
