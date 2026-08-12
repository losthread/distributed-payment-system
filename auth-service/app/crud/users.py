from ..core.config import conn
from ..core.auth import  hash_password, verify_password, create_jwt_token, verify_google_token
from ..models.users import UserProfileResponse, UserProfileUpdate
from psycopg.errors import UniqueViolation, NotNullViolation, CheckViolation, StringDataRightTruncation, InvalidTextRepresentation, OperationalError
from google.auth.exceptions import   GoogleAuthError, TransportError
from fastapi import HTTPException, status
from pydantic import EmailStr
from uuid import UUID

def get_my_profile(user_id: UUID) -> UserProfileResponse:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        SELECT user_id, username, email, created_at, updated_at
        FROM users
        WHERE user_id = %s
      """,
      (user_id,)
    )
    # fetch, commit, close
    row: tuple | None = cursor.fetchone()

    if row is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserProfileResponse(
      user_id = row[0],
      username = row[1],
      email = row[2],
      created_at = row[3],
      updated_at = row[4]
    )

  except OperationalError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

  finally:
    cursor.close()

def update_my_profile(user_id: UUID, profile: UserProfileUpdate) -> UserProfileResponse:
  cursor = conn.cursor()

  try:
    fields = []
    values = []

    if "username" in profile.model_fields_set:
      fields.append("username = %s")
      values.append(profile.username)

    if "email" in profile.model_fields_set:
      fields.append("email = %s")
      values.append(profile.email)

    values.append(user_id)

    cursor.execute(
      f"""
        UPDATE users
        SET {", ".join(fields)}, updated_at = NOW()
        WHERE user_id = %s
        RETURNING user_id, username, email, created_at, updated_at
      """,
      values
    )

    row: tuple | None = cursor.fetchone()

    if row is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    conn.commit()

    return UserProfileResponse(
      user_id = row[0],
      username = row[1],
      email = row[2],
      created_at = row[3],
      updated_at = row[4]
    )

  except UniqueViolation:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or username already exists")

  except OperationalError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

  finally:
    cursor.close()

def delete_my_profile(user_id: UUID) -> dict:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        DELETE FROM users
        WHERE user_id = %s
        RETURNING user_id
      """,
      (user_id,)
    )

    row: tuple | None = cursor.fetchone()

    if row is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    conn.commit()

    return {"message": "Profile deleted successfully"}

  except OperationalError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

  finally:
    cursor.close()