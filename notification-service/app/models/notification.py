from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class NotificationResponse(BaseModel):
  id: UUID
  user_id: UUID
  message: str
  is_read: bool
  created_at: datetime
  updated_at: datetime