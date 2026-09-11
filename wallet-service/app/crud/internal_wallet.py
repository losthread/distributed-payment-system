from ..models.internal_wallet import WalletInternalResponse
from ..kafka.producer import publish_wallet_recharge_failed, publish_wallet_recharge_successful, publish_wallet_withdraw_failed, publish_wallet_withdraw_successful
from ..core.config import conn
from fastapi import HTTPException, status
from uuid import UUID
from psycopg.errors import (
  OperationalError,
  DatabaseError,
  DataError,
  InvalidTextRepresentation,
  NumericValueOutOfRange,
)
from decimal import Decimal

def get_internal_wallet(user_id: UUID) -> WalletInternalResponse:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        SELECT user_id, balance
        FROM wallets
        WHERE user_id = %s
      """,
      (user_id,)
    )
    row: tuple = cursor.fetchone()

    if row is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")

    return WalletInternalResponse(
      user_id=row[0],
      balance=row[1],
    )

  except OperationalError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")

  except DatabaseError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

  finally:
    cursor.close()

def wallet_debit_money(user_id: UUID, amount: Decimal) -> WalletInternalResponse:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        UPDATE wallets
        SET balance = balance - %s, updated_at = NOW()
        WHERE user_id = %s AND balance >= %s
        RETURNING user_id, balance
      """,
      (amount, user_id, amount)
    )
    row: tuple = cursor.fetchone()

    if row is None:
      conn.rollback()
      raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Insufficient balance or wallet not found")

    conn.commit()

    return WalletInternalResponse(
      user_id=row[0],
      balance=row[1],
    )

  except (DataError, InvalidTextRepresentation):
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid wallet data")

  except NumericValueOutOfRange:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount is too large")

  except OperationalError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")

  except DatabaseError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

  finally:
    cursor.close()


def wallet_credit_money(user_id: UUID, amount: Decimal) -> WalletInternalResponse:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        UPDATE wallets
        SET balance = balance + %s, updated_at = NOW()
        WHERE user_id = %s
        RETURNING user_id, balance
      """,
      (amount, user_id)
    )

    row = cursor.fetchone()

    if row is None:
      conn.rollback()
      raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Wallet not found")

    conn.commit()

    return WalletInternalResponse(
      user_id=row[0],
      balance=row[1],
    )

  except (DataError, InvalidTextRepresentation):
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid wallet data")

  except NumericValueOutOfRange:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount is too large")

  except OperationalError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")

  except DatabaseError:
    conn.rollback()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

  finally:
    cursor.close()

### separate functions for depositing and withdraw, to raise notifications ###
### otherwise they would get mispublished for transactions ###
### since the same functions are used for sending money ###
def wallet_deposit(user_id: UUID, amount: Decimal) -> WalletInternalResponse:
  try:
    wallet = wallet_credit_money(user_id, amount)
    publish_wallet_recharge_successful(user_id, amount)

    return wallet

  except HTTPException:
    publish_wallet_recharge_failed(user_id, amount)
    raise


def wallet_withdraw(user_id: UUID, amount: Decimal) -> WalletInternalResponse:
  try:
    wallet = wallet_debit_money(user_id, amount)
    publish_wallet_withdraw_successful(user_id, amount)

    return wallet

  except HTTPException:
    publish_wallet_withdraw_failed(user_id, amount)
    raise