from fastapi import APIRouter, Request
from ..core.client import client
from dotenv import load_dotenv
from uuid import UUID
import os

load_dotenv()

router: APIRouter = APIRouter()

TRANSACTIONS_SERVICE_URL = os.getenv("TRANSACTIONS_SERVICE_URL")

@router.post("/transactions")
async def create_transaction(request: Request):
  body = await request.json()

  response = await client.post(
    f"{TRANSACTIONS_SERVICE_URL}/transactions/",
    headers={
      "Authorization": request.headers.get("Authorization")
    },
    json=body
  )

  return response.json()

@router.get("/transactions")
async def get_transactions(request: Request):
  response = await client.get(
    f"{TRANSACTIONS_SERVICE_URL}/transactions/",
    headers={
      "Authorization": request.headers.get("Authorization")
    }
  )

  return response.json()

@router.get("/transactions/{transaction_id}")
async def get_transaction(transaction_id: UUID, request: Request):
  response = await client.get(
    f"{TRANSACTIONS_SERVICE_URL}/transactions/{transaction_id}",
    headers={
      "Authorization": request.headers.get("Authorization")
    }
  )

  return response.json()