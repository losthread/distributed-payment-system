from pydantic import BaseModel, Field
from typing import Annotated
from decimal import Decimal
from datetime import datetime
from enum import Enum
from uuid import UUID

class TransactionStatus(str, Enum):
  PENDING = "pending"
  COMPLETED = "completed"
  FAILED = "failed"
  REFUND_FAILED = "refund_failed"

class TransactionCreateRequest(BaseModel):
  receiver_id: UUID
  amount: Annotated[Decimal, Field(gt = 0)]

class TransactionResponse(BaseModel):
  transaction_id: UUID
  sender_id: UUID
  receiver_id: UUID
  amount: Decimal
  status: TransactionStatus
  created_at: datetime
  updated_at: datetime
  
class TransactionStatusResponse(BaseModel):
  transaction_id: UUID
  status: TransactionStatus

class TransactionCancelResponse(BaseModel):
  transaction_id: UUID
  status: TransactionStatus