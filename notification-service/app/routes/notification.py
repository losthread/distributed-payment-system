from uuid import UUID
from fastapi import APIRouter, Depends
from ..core.dependencies import get_user_id
from ..crud import notification
from ..models.notification import NotificationResponse

# instantiate API router
router: APIRouter = APIRouter(prefix="/notifications")

@router.get("", response_model=list[NotificationResponse])
async def get_all_notifications(user_id: UUID = Depends(get_user_id)) -> list[NotificationResponse]:
  return notification.get_all_notifications(user_id)

@router.patch("/read-all", response_model=list[NotificationResponse])
async def read_all_notifications(user_id: UUID = Depends(get_user_id)) -> list[NotificationResponse]:
  return notification.read_all_notifications(user_id)

@router.delete("/delete-all")
async def delete_all_notifications(user_id: UUID = Depends(get_user_id)):
  return notification.delete_all_notifications(user_id)

@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(notification_id: UUID, user_id: UUID = Depends(get_user_id)) -> NotificationResponse:
  return notification.get_notification(notification_id, user_id)

@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def read_notification(notification_id: UUID, user_id: UUID = Depends(get_user_id)) -> NotificationResponse:
  return notification.read_notification(notification_id, user_id)

@router.delete("/{notification_id}")
async def delete_notification(notification_id: UUID, user_id: UUID = Depends(get_user_id)):
  return notification.delete_notification(notification_id, user_id)