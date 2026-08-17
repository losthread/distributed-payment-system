from ..core.config import conn
from ..core.auth import  hash_password, verify_password, create_jwt_token, verify_google_token
from ..core.kafka import publish_user_created_event
from psycopg.errors import UniqueViolation, NotNullViolation, CheckViolation, StringDataRightTruncation, InvalidTextRepresentation, OperationalError
from google.auth.exceptions import GoogleAuthError, TransportError
from fastapi import HTTPException, status
from pydantic import EmailStr

def register(username: str | None, email: EmailStr, password: str) -> dict:
  cursor = conn.cursor()

  try:
    # hash entered pass
    hashed_password = hash_password(password)

    cursor.execute(
      """
        INSERT INTO users(username, email, hashed_password)
        VALUES (%s, %s, %s)
        RETURNING user_id
      """,
      (username, email, hashed_password)
    )
    # fetch, commit, close
    row: tuple = cursor.fetchone()
    conn.commit()

    # publish event to kafka message queue
    publish_user_created_event(str(row[0]))

    return {"user_id": row[0]}

  # email/username already exists
  except UniqueViolation:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or username already exists")

  # username and email are both NULL
  except CheckViolation:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email is required")

  # database connection/server error
  except OperationalError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

  finally:
    cursor.close()

def login(login_identifier: str, password: str):
  cursor = conn.cursor()

  try:
    # check if user is registered
    cursor.execute(
      """
        SELECT user_id, hashed_password
        FROM users
        WHERE email = %s OR username = %s
      """,
      (login_identifier, login_identifier)
    )
    row: tuple = cursor.fetchone()

    print("LOGIN:", repr(login_identifier))
    print("ROW:", row)

    if row is None:
      conn.rollback()
      cursor.close()
      raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Account is not registered! Register first")

    user_id: str = row[0]
    stored_password_hash: str = row[1]

    if not verify_password(password, stored_password_hash):
      raise HTTPException(status_code = 401, detail = "Email or password is incorrect")
    
    # create token 
    token = create_jwt_token(user_id)

    return {
      "access_token": token,
      "token_type": "bearer",
      "user_id": user_id
    }

  # database connection/server error
  except OperationalError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

  # invalid PostgreSQL value/type
  except InvalidTextRepresentation:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid login identifier")

  finally:
    cursor.close()

def google_login(google_token: str):
  cursor = conn.cursor()

  try:
    # verify token with google
    id_info = verify_google_token(google_token)

    if not id_info:
      cursor.close()
      raise HTTPException(status_code=401, detail="Invalid Google Token")
    
    email = id_info["email"]

    # check if user already exists
    cursor.execute(
      """
        SELECT user_id
        FROM users
        WHERE email = %s
      """,
      (email,)
    )
    row = cursor.fetchone()

    if row is None:
      # create user in DB if it doesnt exist
      cursor.execute(
        """
          INSERT INTO users(username, email, hashed_password, created_at)
          VALUES (%s, %s, %s, NOW())
          RETURNING user_id
        """,
        (email.split("@")[0], email, None)
      )
      row = cursor.fetchone()
      conn.commit()

    user_id = row[0]

    # create JWT
    token = create_jwt_token(user_id)

    return {
      "access_token": token,
      "token_type": "bearer",
      "user_id": user_id
    }

  # handle db errors
  except ValueError:
    conn.rollback()
    raise HTTPException(status_code=401, detail="Invalid Google token")

  # email already exists due to a race condition
  except UniqueViolation:
    conn.rollback()
    raise HTTPException(status_code=409, detail="Email already exists")

  # required DB field is missing
  except NotNullViolation:
    conn.rollback()
    raise HTTPException(status_code=400, detail="Required field is missing")

  # database unavailable
  except OperationalError:
    conn.rollback()
    raise HTTPException(status_code=500, detail="Database error")

  finally:
    cursor.close()