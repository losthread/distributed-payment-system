from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import datetime
from uuid import UUID

class UserProfileResponse(BaseModel):
  user_id: UUID
  username: str | None = None
  email: EmailStr
  created_at: datetime
  updated_at: datetime

class UserProfileUpdate(BaseModel):
  username: Annotated[str, Field(min_length=1)] | None = None
  email: EmailStr | None = None

  @model_validator(mode="after")
  def at_least_one_field(self):
    if self.username is None and self.email is None:
      raise ValueError("At least one field must be provided")

    return self