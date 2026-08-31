from ..models.transactions import TransactionResponse
from psycopg.errors import OperationalError, DatabaseError
from ..kafka.producer import publish_refund_event
from ..core.config import conn
from fastapi import HTTPException, status
from ..core.client import client
from dotenv import load_dotenv
from decimal import Decimal
from uuid import UUID
import httpx
import os

# load env variables
load_dotenv()

INTERNAL_SERVICE_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN")

def create_pending_transaction(sender_id: UUID, receiver_id: UUID, amount: Decimal) -> UUID:
  cursor = conn.cursor()

  # insert pending transaction in db
  try:
    cursor.execute(
      """
        INSERT INTO transactions (sender_id, receiver_id, amount)
        VALUES (%s, %s, %s)
        RETURNING transaction_id
      """,
      (sender_id, receiver_id, amount)
    )
    row = cursor.fetchone()
    transaction_id = row[0]
    conn.commit()

    return transaction_id

  except OperationalError as e:
    conn.rollback()
    print("OPERATIONAL ERROR:", repr(e))
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database service unavailable")

  except DatabaseError as e:
    conn.rollback()
    print("DATABASE ERROR:", repr(e))
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

  finally:
    cursor.close()

def update_transaction_status(transaction_id: UUID, transaction_status: str) -> None:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        UPDATE transactions
        SET status = %s, updated_at = NOW()
        WHERE transaction_id = %s
      """,
      (transaction_status, transaction_id)
    )

    conn.commit()

  except OperationalError as e:
    conn.rollback()
    print("OPERATIONAL ERROR:", repr(e))
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database service unavailable")

  except DatabaseError as e:
    conn.rollback()
    print("DATABASE ERROR:", repr(e))
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

  finally:
    cursor.close()

async def create_transaction(sender_id: UUID, receiver_id: UUID, amount: Decimal) -> TransactionResponse:
  print("CREATE TRANSACTION ROUTE HIT")
  # debit sender(if fail = transaction fail) ->
  # -> credit receiver (if fail, refund sender) ->
  # -> refund sender (id fail, kafka event refund in a separate thread)

  transaction_id = create_pending_transaction(sender_id, receiver_id, amount)
  # debit sender's account
  try:
    debit_response = await client.post(
      f"http://localhost:8001/internal/wallets/{sender_id}/debit",
      headers={
        "Authorization": f"Bearer {INTERNAL_SERVICE_TOKEN}"
      },
      json={
        "amount": str(amount)
      }
    )

    debit_response.raise_for_status()

  # debit failed -> set transaction status as failed
  except httpx.HTTPStatusError as e:
    print("HTTP ERROR:", repr(e))
    update_transaction_status(transaction_id, "failed")
    raise HTTPException(status_code = e.response.status_code, detail = e.response.json().get("detail", "Debit failed"))

  # credit the receiver if debit succeeds
  try:
    credit_response = await client.post(
      f"http://localhost:8001/internal/wallets/{receiver_id}/credit",
      headers={
        "Authorization": f"Bearer {INTERNAL_SERVICE_TOKEN}"
      },
      json={
        "amount": str(amount)
      }
    )

    credit_response.raise_for_status()
    # transaction complete
    update_transaction_status(transaction_id, "completed")

    transaction = get_transaction(transaction_id, sender_id)

    return transaction

  except httpx.RequestError as e:
    # refund using internal api -> if fail -> send kafka event to repeat this 3 times
    try:
      credit_response = await client.post(
        f"http://localhost:8001/internal/wallets/{sender_id}/credit",
        headers={
          "Authorization": f"Bearer {INTERNAL_SERVICE_TOKEN}"
        },
        json={
          "amount": str(amount)
        }
      )

      credit_response.raise_for_status()
      # transaction complete
      update_transaction_status(transaction_id, "failed")

    except httpx.HTTPStatusError as e:
      # interbnal api refund fails
      update_transaction_status(transaction_id, "refund_failed")

      # send kafka event for refunding as a fallback
      publish_refund_event(
        transaction_id,
        sender_id,
        amount
      )
      status_code = e.response.status_code if e.response else 503

      raise HTTPException(
        status_code=status_code,
        detail="Payment failed. Refund has been initiated."
      )
    
    raise HTTPException(status_code = e.response.status_code, detail = e.response.json().get("detail", "Credit failed, refunding money to the sender"))

def get_transaction(transaction_id: UUID, user_id: UUID) -> TransactionResponse:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        SELECT transaction_id, sender_id, receiver_id, amount, status, created_at, updated_at
        FROM transactions
        WHERE transaction_id = %s AND (sender_id = %s OR receiver_id = %s)
      """,
      (transaction_id, user_id, user_id)
    )
    row = cursor.fetchone()

    if row is None:
      raise HTTPException(status_code=404, detail="Transaction not found")

    return TransactionResponse(
      transaction_id=row[0],
      sender_id=row[1],
      receiver_id=row[2],
      amount=row[3],
      status=row[4],
      created_at=row[5],
      updated_at=row[6]
    )

  except OperationalError as e:
    conn.rollback()
    print("OPERATIONAL ERROR:", repr(e))
    raise HTTPException(status_code=503, detail="Database unavailable")

  except DatabaseError as e:
    conn.rollback()
    print("DATABASE ERROR:", repr(e))
    raise HTTPException(status_code=500, detail="Database error")

  finally:
    cursor.close()

def get_transactions(user_id: UUID) -> list[TransactionResponse]:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        SELECT transaction_id, sender_id, receiver_id, amount, status, created_at, updated_at
        FROM transactions
        WHERE sender_id = %s OR receiver_id = %s
        ORDER BY created_at DESC
      """,
      (user_id, user_id)
    )
    rows = cursor.fetchall()

    return [
      TransactionResponse(
        transaction_id=row[0],
        sender_id=row[1],
        receiver_id=row[2],
        amount=row[3],
        status=row[4],
        created_at=row[5],
        updated_at=row[6]
      )
      for row in rows
    ]

  except OperationalError as e:
    conn.rollback()
    print("OPERATIONAL ERROR:", repr(e))
    raise HTTPException(status_code=503, detail="Database unavailable")

  except DatabaseError as e:
    conn.rollback()
    print("DATABASE ERROR:", repr(e))
    raise HTTPException(status_code=500, detail="Database error")

  finally:
    cursor.close()