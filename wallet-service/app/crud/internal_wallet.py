from ..models.internal_wallet import WalletInternalResponse
from ..core.config import conn
from fastapi import HTTPException, status
from uuid import UUID
from decimal import Decimal

def get_internal_wallet(user_id: UUID) -> WalletInternalResponse:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        SELECT user_id, balance, currency
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
      currency=row[2]
    )

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
        RETURNING user_id, balance, currency
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
      currency=row[2]
    )

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
        RETURNING user_id, balance, currency
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
      currency=row[2]
    )

  finally:
    cursor.close()