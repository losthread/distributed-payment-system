# Notification Service API

**Base URL:** `/notifications`

## Endpoints

### GET `/notifications`

Get all notifications for authenticated user.

**Auth:** JWT token required

**Response:**

```json
{
  "notifications": [
    {
      "notification_id": "uuid",
      "user_id": "uuid",
      "message": "string",
      "is_read": false,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### PATCH `/notifications/read-all`

Mark all notifications as read for authenticated user.

**Auth:** JWT token required

**Response:**

```json
{
  "notifications": [
    {
      "notification_id": "uuid",
      "user_id": "uuid",
      "message": "string",
      "is_read": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### DELETE `/notifications/delete-all`

Delete all notifications for authenticated user.

**Auth:** JWT token required

**Response:**

```json
{
  "message": "Notifications deleted",
  "deleted_count": 0
}
```

### GET `/notifications/{notification_id}`

Get specific notification by ID.

**Auth:** JWT token required

**Response:**

```json
{
  "notification_id": "uuid",
  "user_id": "uuid",
  "message": "string",
  "is_read": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### PATCH `/notifications/{notification_id}/read`

Mark specific notification as read.

**Auth:** JWT token required

**Response:**

```json
{
  "notification_id": "uuid",
  "user_id": "uuid",
  "message": "string",
  "is_read": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### DELETE `/notifications/{notification_id}`

Delete specific notification by ID.

**Auth:** JWT token required

**Response:**

```json
{
  "message": "Notification deleted"
}