from fastapi import APIRouter, Depends
from ..models.users import UserProfileResponse, UserProfileUpdate
from ..core.dependencies import get_user_id
from ..crud import users
from uuid import UUID

router = APIRouter(prefix = "/users")

@router.get('/profile', response_model = UserProfileResponse)
async def get_my_profile(user_id: UUID = Depends(get_user_id)) -> UserProfileResponse:
  return users.get_my_profile(user_id)

@router.patch('/profile', response_model=UserProfileResponse)
async def update_my_profile(profile: UserProfileUpdate, user_id: UUID = Depends(get_user_id)) -> UserProfileResponse:
  return users.update_my_profile(user_id, profile)

@router.delete('/profile')
async def delete_my_profile(user_id: UUID = Depends(get_user_id)) -> dict:
  return users.delete_my_profile(user_id)