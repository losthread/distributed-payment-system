from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
import jwt
import os

# load env variables
load_dotenv()

JWT_SECRET: str = os.getenv("JWT_KEY")
ALGORITHM: str = "HS256"

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