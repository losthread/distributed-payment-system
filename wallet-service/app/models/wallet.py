from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime
from decimal import Decimal
from uuid import UUID

class WalletResponse(BaseModel):
  id: int
  user_id: UUID
  balance: Annotated[Decimal, Field(decimal_places=2)]
  currency: Annotated[str, Field(min_length=3, max_length=3)]
  created_at: datetime
  updated_at: datetime

class WalletBalanceResponse(BaseModel):
  balance: Annotated[Decimal, Field(decimal_places=2)]
  currency: Annotated[str, Field(min_length=3, max_length=3)]