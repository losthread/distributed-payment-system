from fastapi import APIRouter, Request
from ..core.client import client
from dotenv import load_dotenv
import os

load_dotenv()

# instantiate API router
router: APIRouter = APIRouter()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")

@router.post("/auth/register")
async def register(request: Request):
  body = await request.json()

  response = await client.post(
    f"{AUTH_SERVICE_URL}/auth/register",
    json=body
  )

  return response.json()

@router.post("/auth/login")
async def login(request: Request):
  body = await request.json()

  response = await client.post(
    f"{AUTH_SERVICE_URL}/auth/login",
    json=body
  )

  return response.json()

@router.post("/auth/login/google")
async def google_login(request: Request):
  body = await request.json()

  response = await client.post(
    f"{AUTH_SERVICE_URL}/auth/login/google",
    json=body
  )

  return response.json()

@router.get("/users/profile")
async def get_profile(request: Request):
  response = await client.get(
    f"{AUTH_SERVICE_URL}/users/profile",
    headers={
      "Authorization": request.headers.get("Authorization")
    }
  )

  return response.json()

@router.patch("/users/profile")
async def update_profile(request: Request):
  body = await request.json()

  response = await client.patch(
    f"{AUTH_SERVICE_URL}/users/profile",
    headers={
      "Authorization": request.headers.get("Authorization")
    },
    json=body
  )

  return response.json()

@router.delete("/users/profile")
async def delete_profile(request: Request):
  response = await client.delete(
    f"{AUTH_SERVICE_URL}/users/profile",
    headers={
      "Authorization": request.headers.get("Authorization")
    }
  )

  return response.json()