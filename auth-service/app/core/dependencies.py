from fastapi import HTTPException, Header
from .auth import decode_jwt_token

# exract user_id from http header
def get_user_id(authorization: str = Header(None)):
  if not authorization or not authorization.startswith("Bearer "):
    raise HTTPException(status_code = 401, detail = "Missing or invalid token")

  token: str = authorization.split(" ")[1]
  user_id: str = decode_jwt_token(token)

  if user_id is None:
    raise HTTPException(status_code = 401, detail = "Invalid or expired token")

  return user_id