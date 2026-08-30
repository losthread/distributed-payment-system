from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Annotated
from datetime import datetime
from uuid import UUID

class WalletInternalResponse(BaseModel):
  user_id: UUID
  balance: Decimal

class WalletDebitRequest(BaseModel):
  amount: Annotated[Decimal, Field(gt = 0)]

class WalletCreditRequest(BaseModel):
  amount: Annotated[Decimal, Field(gt = 0)]

class WalletResponse(BaseModel):
  id: int
  user_id: UUID
  balance: Decimal
  created_at: datetime
  updated_at: datetime

class WalletBalanceResponse(BaseModel):
  balance: Decimal