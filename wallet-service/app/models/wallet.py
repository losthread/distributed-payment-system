from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime
from decimal import Decimal
from uuid import UUID

class WalletResponse(BaseModel):
  id: int
  user_id: UUID
  balance: Annotated[Decimal, Field(decimal_places=2)]
  created_at: datetime
  updated_at: datetime

class WalletBalanceResponse(BaseModel):
  balance: Annotated[Decimal, Field(decimal_places=2)]

class WalletAmountRequest(BaseModel):
  amount: Annotated[Decimal, Field(gt=0)]