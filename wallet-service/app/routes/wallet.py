from fastapi import APIRouter, Depends
from ..models.wallet import WalletResponse, WalletBalanceResponse
from ..crud import wallet
from ..core.dependencies import get_user_id
from uuid import UUID

# instantiate router
router: APIRouter = APIRouter(prefix = "/wallets")

@router.get("", response_model = WalletResponse)
async def get_my_wallet(user_id: UUID = Depends(get_user_id)) -> WalletResponse:
  return wallet.get_my_wallet(user_id)

@router.get("/balance", response_model = WalletBalanceResponse)
async def get_my_wallet_balance(user_id: UUID = Depends(get_user_id)) -> WalletBalanceResponse:
  return wallet.get_my_wallet_balance(user_id) 