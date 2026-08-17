from fastapi import APIRouter, Depends
from ..models.internal_wallet import WalletInternalResponse, WalletCreditRequest, WalletDebitRequest
from ..core.internal_dependency import verify_internal_token
from ..crud import internal_wallet
from uuid import UUID

# instantiate router
router: APIRouter = APIRouter(prefix="/internal")

@router.get("/wallets/{user_id}", response_model = WalletInternalResponse, dependencies=[Depends(verify_internal_token)])
async def get_internal_wallet(user_id: UUID) -> WalletInternalResponse:
  return internal_wallet.get_internal_wallet(user_id)

@router.post("/wallets/{user_id}/debit", response_model = WalletInternalResponse, dependencies=[Depends(verify_internal_token)])
async def wallet_debit(user_id: UUID, request: WalletDebitRequest) -> WalletInternalResponse:
  return internal_wallet.wallet_debit_money(user_id, request.amount)

@router.post("/wallets/{user_id}/credit", response_model = WalletInternalResponse, dependencies=[Depends(verify_internal_token)])
async def wallet_credit(user_id: UUID, request: WalletCreditRequest) -> WalletInternalResponse:
  return internal_wallet.wallet_credit_money(user_id, request.amount)