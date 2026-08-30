from fastapi import APIRouter, Depends
from ..models.wallet import WalletResponse, WalletBalanceResponse, WalletAmountRequest
from ..crud import wallet, internal_wallet
from ..core.dependencies import get_user_id
from decimal import Decimal
from uuid import UUID

# instantiate router
router: APIRouter = APIRouter(prefix = "/wallets")

@router.get("", response_model = WalletResponse)
async def get_my_wallet(user_id: UUID = Depends(get_user_id)) -> WalletResponse:
  return wallet.get_my_wallet(user_id)

@router.get("/balance", response_model = WalletBalanceResponse)
async def get_my_wallet_balance(user_id: UUID = Depends(get_user_id)) -> WalletBalanceResponse:
  return wallet.get_my_wallet_balance(user_id) 

@router.post("/deposit", response_model = WalletBalanceResponse)
async def deposit_money(amount: WalletAmountRequest, user_id: UUID = Depends(get_user_id)) -> WalletBalanceResponse:
  return internal_wallet.wallet_credit_money(user_id, amount.amount)

@router.post("/withdraw", response_model = WalletBalanceResponse)
async def deposit_money(amount: WalletAmountRequest, user_id: UUID = Depends(get_user_id)) -> WalletBalanceResponse:
  return internal_wallet.wallet_debit_money(user_id, amount.amount)