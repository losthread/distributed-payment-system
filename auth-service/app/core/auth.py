from dotenv import load_dotenv
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
import os

# load env variables
load_dotenv()

# JWT auth
JWT_SECRET: str = os.getenv("JWT_KEY")
ALGORITHM: str = "HS256"

# instantiate password hasher
ph: PasswordHasher = PasswordHasher()

# hash the password entered when registering
def hash_password(password: str) -> str:
  return ph.hash(password)

# verify login password with stored hash in DB
def verify_password(password: str, stored_hash: str) -> bool:
  try:
    ph.verify(stored_hash, password)
    return True

  except (VerifyMismatchError, VerificationError, InvalidHash):
    return False

# create JWT token
def create_jwt_token(user_id: str) -> str:
  # JWT structure (base64) header.payload.signature

  payload: dict = {
    "user_id": str(user_id),
    "exp": datetime.now(timezone.utc) + timedelta(days=7)
  }

  # return final JWT string
  token: str = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
  return token

# extract user_id from received token
def decode_jwt_token(token: str) -> str | None:
  try:
    payload: str = jwt.decode(
      token,
      JWT_SECRET,
      algorithms=[ALGORITHM] 
    )

    return payload.get("user_id")

  except InvalidTokenError as e:
    print(f"Invalid JWT Token: {e}")
    return None

# GOOGLE OAuth2
GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")

def verify_google_token(token: str) -> dict | None:
  try:
    id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
    return id_info
  
  except Exception:
    return None