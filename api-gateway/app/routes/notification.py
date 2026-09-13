from fastapi import APIRouter, Request
from ..core.client import client
from dotenv import load_dotenv
from uuid import UUID
import os

load_dotenv()

router: APIRouter = APIRouter()

NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL")

@router.get("/notifications")
async def get_notifications(request: Request):

  response = await client.get(
    f"{NOTIFICATION_SERVICE_URL}/notifications",
    headers={
      "Authorization": request.headers.get("Authorization")
    }
  )

  return response.json()

@router.patch("/notifications/read-all")
async def read_all_notifications(request: Request):

  response = await client.patch(
    f"{NOTIFICATION_SERVICE_URL}/notifications/read-all",
    headers={
      "Authorization": request.headers.get("Authorization")
    }
  )

  return response.json()

@router.delete("/notifications/delete-all")
async def delete_all_notifications(request: Request):

  response = await client.delete(
    f"{NOTIFICATION_SERVICE_URL}/notifications/delete-all",
    headers={
      "Authorization": request.headers.get("Authorization")
    }
  )

  return response.json()

@router.get("/notifications/{notification_id}")
async def get_notification(notification_id: UUID, request: Request):

  response = await client.get(
    f"{NOTIFICATION_SERVICE_URL}/notifications/{notification_id}",
    headers={
      "Authorization": request.headers.get("Authorization")
    }
  )

  return response.json()

@router.patch("/notifications/{notification_id}/read")
async def read_notification(notification_id: UUID, request: Request):

  response = await client.patch(
    f"{NOTIFICATION_SERVICE_URL}/notifications/{notification_id}/read",
    headers={
      "Authorization": request.headers.get("Authorization")
    }
  )

  return response.json()

@router.delete("/notifications/{notification_id}")
async def delete_notification(notification_id: UUID, request: Request):

  response = await client.delete(
    f"{NOTIFICATION_SERVICE_URL}/notifications/{notification_id}",
    headers={
      "Authorization": request.headers.get("Authorization")
    }
  )

  return response.json()