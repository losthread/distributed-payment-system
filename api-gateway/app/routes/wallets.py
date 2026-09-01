from fastapi import APIRouter, Request
from ..core.client import client
from dotenv import load_dotenv
import os

load_dotenv()

# instantiate API router
router: APIRouter = APIRouter()

WALLET_SERVICE_URL = os.getenv("WALLET_SERVICE_URL")

@router.get("/wallets")
async def get_my_wallet(request: Request):
  response = await client.get(
    f"{WALLET_SERVICE_URL}/wallets",
    headers={
      "Authorization": request.headers.get("Authorization")
    }
  )

  return response.json()

@router.get("/wallets/balance")
async def get_my_wallet_balance(request: Request):
  response = await client.get(
    f"{WALLET_SERVICE_URL}/wallets/balance",
    headers={
      "Authorization": request.headers.get("Authorization")
    }
  )

  return response.json()

@router.post("/wallets/deposit")
async def deposit_money(request: Request):
  body = await request.json()

  response = await client.post(
    f"{WALLET_SERVICE_URL}/wallets/deposit",
    headers={
      "Authorization": request.headers.get("Authorization")
    },
    json=body
  )

  return response.json()

@router.post("/wallets/withdraw")
async def withdraw_money(request: Request):
  body = await request.json()

  response = await client.post(
    f"{WALLET_SERVICE_URL}/wallets/withdraw",
    headers={
      "Authorization": request.headers.get("Authorization")
    },
    json=body
  )

  return response.json()