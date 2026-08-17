from fastapi import Header, HTTPException
import os

def verify_internal_token(authorization: str = Header(None)) -> None:
  if authorization != f"Bearer {os.getenv('INTERNAL_SERVICE_TOKEN')}":
    raise HTTPException(status_code=401, detail="Unauthorized service")