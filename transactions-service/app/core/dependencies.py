from fastapi import HTTPException, Header
from uuid import UUID
from .auth import decode_jwt_token

def get_user_id(authorization: str = Header(None)) -> UUID:
  if not authorization or not authorization.startswith("Bearer "):
    raise HTTPException(status_code=401, detail="Missing or invalid token")

  token = authorization.split(" ")[1]

  user_id = decode_jwt_token(token)

  if user_id is None:
    raise HTTPException(status_code=401, detail="Invalid or expired token")

  return UUID(user_id)