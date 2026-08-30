from fastapi import APIRouter, Depends
from ..models.transactions import TransactionCreateRequest, TransactionResponse
from ..core.dependencies import get_user_id
from ..crud import transactions
from uuid import UUID

# instantiate api router
router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model = TransactionResponse)
async def create_transaction(data: TransactionCreateRequest, user_id: UUID = Depends(get_user_id)) -> TransactionResponse:
  return await transactions.create_transaction(sender_id = user_id, receiver_id = data.receiver_id, amount = data.amount)

@router.get("/", response_model = list[TransactionResponse])
async def get_transactions(user_id: UUID = Depends(get_user_id)) -> list[TransactionResponse]:
  return transactions.get_transactions(user_id)

@router.get("/{transaction_id}", response_model = TransactionResponse)
async def get_transaction(transaction_id: UUID, user_id: UUID = Depends(get_user_id)) -> TransactionResponse:
  return transactions.get_transaction(transaction_id, user_id)