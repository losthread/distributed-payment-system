from fastapi import HTTPException, status
from psycopg.errors import OperationalError, DatabaseError 
from ..core.config import conn
from ..models.wallet import WalletResponse, WalletBalanceResponse
from uuid import UUID

def create_wallet(user_id: UUID) -> bool:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        INSERT INTO wallets(user_id)
        VALUES (%s)
      """,
      (user_id,)
    )
    conn.commit()

    return cursor.rowcount > 0

  except OperationalError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")

  except DatabaseError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

  finally:
    cursor.close()

def get_my_wallet(user_id: UUID) -> WalletResponse | None:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        SELECT id, user_id, balance, created_at, updated_at
        FROM wallets
        WHERE user_id = %s
      """,
      (user_id,)
    )

    row = cursor.fetchone()

    if row is None:
      raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Wallet for user: {user_id} doesn't exist")

    return WalletResponse(
      id=row[0],
      user_id=row[1],
      balance=row[2],
      created_at=row[3],
      updated_at=row[4]
    )

  except OperationalError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")

  except DatabaseError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

  finally:
    cursor.close()

def get_my_wallet_balance(user_id: UUID) -> WalletBalanceResponse | None:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        SELECT balance
        FROM wallets
        WHERE user_id = %s
      """,
      (user_id,)
    )

    row = cursor.fetchone()

    if row is None:
      return None

    return WalletBalanceResponse(
      balance=row[0]
    )

  except OperationalError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")

  except DatabaseError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

  finally:
    cursor.close()